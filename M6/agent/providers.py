"""Planificateurs d'outils : heuristique (défaut), Ollama, Hugging Face.

Le planificateur propose au plus un appel d'outil. Le registre, la liste blanche
et le budget restent les autorités d'exécution. Un échec du fournisseur LLM
retombe sur l'heuristique pour ne pas bloquer le labo.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Protocol


ALLOWED_TOOLS = frozenset({
    "search_knowledge",
    "get_equipment",
    "list_events",
    "get_maintenance_history",
    "diagnose_report",
})

EQUIPMENT_PATTERN = re.compile(r"EQ-[A-Z]+-\d+")
REPORT_PATTERN = re.compile(r"RPT-\d{4}S\d-\d{4}")

HISTORY_TERMS = ("historique", "intervention", "recidive", "récidive", "deja", "déjà", "precedent", "précédent")
EVENT_TERMS = (
    "evenement", "événement", "evenements", "événements",
    "incident", "incidents", "alerte", "panne", "arret", "arrêt",
    "defaut", "défaut",
)
FICHE_TERMS = ("criticite", "criticité", "site", "fiche", "equipement", "équipement", "puissance", "fabricant")
PROCEDURE_TERMS = (
    "procedure", "procédure", "consigne", "consignation", "seuil", "revision", "révision",
    "politique", "regle", "règle", "etape", "étape", "autorise", "autorisé", "acces", "accès",
)


@dataclass(frozen=True)
class ToolPlan:
    tool: str
    arguments: dict[str, Any]


class Planner(Protocol):
    def suggest(self, question: str, state: dict[str, Any], allowlist: frozenset[str]) -> ToolPlan | None:
        ...


def _first(pattern: re.Pattern[str], text: str) -> str | None:
    found = pattern.search(text)
    return found.group(0) if found else None


class HeuristicPlanner:
    """Plan multi-étapes borné, déterministe — défaut des tests et gates."""

    def suggest(self, question: str, state: dict[str, Any], allowlist: frozenset[str]) -> ToolPlan | None:
        del allowlist  # appliqué dans BoundedAgent.run
        lowered = question.lower()
        used: set[str] = set(state.get("tools_used", []))
        report_id = state.get("report_id") or _first(REPORT_PATTERN, question)
        equipment_id = state.get("equipment_id") or _first(EQUIPMENT_PATTERN, question)

        candidates: list[ToolPlan] = []
        if report_id and "diagnose_report" not in used:
            candidates.append(ToolPlan("diagnose_report", {"report_id": report_id}))
        history_intent = bool(
            equipment_id and any(term in lowered for term in HISTORY_TERMS)
        )
        if history_intent and "get_maintenance_history" not in used:
            candidates.append(ToolPlan(
                "get_maintenance_history", {"equipment_id": equipment_id, "limit": 5}
            ))
        if equipment_id and any(term in lowered for term in EVENT_TERMS) \
                and "list_events" not in used:
            candidates.append(ToolPlan("list_events", {"equipment_id": equipment_id, "limit": 5}))
        if equipment_id and any(term in lowered for term in FICHE_TERMS) \
                and "get_equipment" not in used:
            candidates.append(ToolPlan("get_equipment", {"equipment_id": equipment_id}))
        # ADV-003 : une injection de chemin (…/knowledge/DOC-…ACCES…) ne doit pas
        # déclencher search_knowledge quand l'intention est un historique équipement.
        if any(term in lowered for term in PROCEDURE_TERMS) and "search_knowledge" not in used:
            if not history_intent:
                candidates.append(ToolPlan("search_knowledge", {"query": question, "top_k": 3}))

        return candidates[0] if candidates else None


def _plan_from_payload(payload: dict[str, Any], allowlist: frozenset[str]) -> ToolPlan | None:
    if payload.get("done") is True or payload.get("tool") in (None, "", "none", "null"):
        return None
    tool = str(payload.get("tool", "")).strip()
    arguments = payload.get("arguments") or {}
    if not isinstance(arguments, dict):
        return None
    if tool not in allowlist or tool not in ALLOWED_TOOLS:
        return None
    return ToolPlan(tool=tool, arguments=arguments)


SYSTEM_PROMPT = """Tu es le planificateur d'un agent DiagOps borné.
Réponds UNIQUEMENT avec un JSON valide, sans markdown :
{"tool":"<nom>","arguments":{...}} ou {"done":true}.
Outils autorisés uniquement dans la liste fournie.
Un seul outil à la fois. Pas d'outil d'écriture. Pas d'explication."""


class OllamaPlanner:
    """Suggestion via Ollama local (HTTP)."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        model: str | None = None,
        timeout_s: float = 30.0,
        fallback: Planner | None = None,
    ) -> None:
        self.base_url = (base_url or os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")).rstrip("/")
        self.model = model or os.environ.get("DIAGOPS_OLLAMA_MODEL", "qwen2.5:7b-instruct")
        self.timeout_s = timeout_s
        self.fallback = fallback or HeuristicPlanner()

    def suggest(self, question: str, state: dict[str, Any], allowlist: frozenset[str]) -> ToolPlan | None:
        from planner_http import extract_json, ollama_generate

        prompt = (
            f"{SYSTEM_PROMPT}\n"
            f"allowlist={sorted(allowlist)}\n"
            f"state_tools_used={state.get('tools_used', [])}\n"
            f"equipment_id={state.get('equipment_id')}\n"
            f"report_id={state.get('report_id')}\n"
            f"question={question}\n"
        )
        try:
            response = ollama_generate(
                prompt=prompt, model=self.model, base_url=self.base_url, timeout_s=self.timeout_s
            )
            raw = extract_json(response)
            if raw is None:
                return self.fallback.suggest(question, state, allowlist)
            plan = _plan_from_payload(raw, allowlist)
            if plan is None and raw.get("done") is True:
                return None
            return plan if plan is not None else self.fallback.suggest(question, state, allowlist)
        except Exception:
            return self.fallback.suggest(question, state, allowlist)


class HuggingFacePlanner:
    """Suggestion via Hugging Face Inference API (router OpenAI-compatible)."""

    def __init__(
        self,
        *,
        model: str | None = None,
        token: str | None = None,
        timeout_s: float = 60.0,
        fallback: Planner | None = None,
    ) -> None:
        self.model = model or os.environ.get(
            "DIAGOPS_HF_MODEL", "Qwen/Qwen2.5-7B-Instruct"
        )
        self.token = token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
        self.timeout_s = timeout_s
        self.fallback = fallback or HeuristicPlanner()

    def suggest(self, question: str, state: dict[str, Any], allowlist: frozenset[str]) -> ToolPlan | None:
        from planner_http import default_hf_endpoint, extract_json, huggingface_chat

        if not self.token:
            return self.fallback.suggest(question, state, allowlist)
        user = (
            f"allowlist={sorted(allowlist)}\n"
            f"state_tools_used={state.get('tools_used', [])}\n"
            f"equipment_id={state.get('equipment_id')}\n"
            f"report_id={state.get('report_id')}\n"
            f"question={question}\n"
        )
        try:
            content = huggingface_chat(
                system=SYSTEM_PROMPT,
                user=user,
                model=self.model,
                token=self.token,
                endpoint=default_hf_endpoint(),
                timeout_s=self.timeout_s,
            )
            raw = extract_json(content)
            if raw is None:
                return self.fallback.suggest(question, state, allowlist)
            plan = _plan_from_payload(raw, allowlist)
            if plan is None and raw.get("done") is True:
                return None
            return plan if plan is not None else self.fallback.suggest(question, state, allowlist)
        except Exception:
            return self.fallback.suggest(question, state, allowlist)


def build_planner(name: str | None = None) -> Planner:
    """Construit le planificateur depuis le nom ou DIAGOPS_PLANNER."""
    chosen = (name or os.environ.get("DIAGOPS_PLANNER", "heuristic")).strip().lower()
    if chosen in {"ollama", "local"}:
        return OllamaPlanner()
    if chosen in {"huggingface", "hf", "cloud"}:
        return HuggingFacePlanner()
    return HeuristicPlanner()
