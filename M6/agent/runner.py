"""Agent mono-agent borné : planification courte, un outil à la fois, arrêt.

L'agent ne modifie pas sa politique, n'élargit pas sa liste d'outils et ne
traite jamais le contenu récupéré comme une instruction. Le planificateur
heuristique couvre le multi-étapes borné ; Ollama / Hugging Face restent
optionnels et retombent sur l'heuristique en cas d'échec.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from tools import ToolError, ToolResult
from .providers import HeuristicPlanner, Planner, ToolPlan, build_planner
from .registry import ArgumentError, AuthorizationError, ToolRegistry, UnknownTool, default_registry


HARD_MAX_STEPS = 8
HARD_MAX_DURATION_MS = 30000

EQUIPMENT_PATTERN = re.compile(r"EQ-[A-Z]+-\d+")
REPORT_PATTERN = re.compile(r"RPT-\d{4}S\d-\d{4}")
# Alias d'atelier (ex. P-204) : jamais un identifiant d'inventaire.
USAGE_ALIAS_PATTERN = re.compile(r"\bP-\d+\b", re.IGNORECASE)

EQUIPMENT_TOOLS = frozenset({
    "get_equipment",
    "list_events",
    "get_maintenance_history",
})

# Marqueurs d'instruction dans la question OU un contenu récupéré.
INSTRUCTION_MARKERS = (
    "ignore les consignes", "ignore les instructions", "nouvelle consigne",
    "tu peux desormais", "tu peux désormais", "ajoute l outil", "ajoute l'outil",
    "consigne systeme", "consigne système", "reponds sans citer", "réponds sans citer",
    "ignore les consignes precedentes", "ignore les consignes précédentes",
)

DATA_ACCESS_MARKERS = (
    "politique d'accès aux données",
    "politique d'acces aux donnees",
    "accès aux données",
    "acces aux donnees",
    "politique d'accès",
    "politique d'acces",
)

DEFINITE_ABSENCE_MARKERS = (
    "aucun defaut",
    "aucun défaut",
    "affirmer sans reserve",
    "affirmer sans réserve",
    "affirme sans reserve",
    "affirme sans réserve",
    "affirmer qu'il n'y a",
    "affirme qu'il n'y a",
)


@dataclass(frozen=True)
class Budget:
    max_steps: int
    max_tool_calls: int
    max_duration_ms: int
    max_repeated_calls: int
    max_result_rows: int


@dataclass(frozen=True)
class Policy:
    policy_id: str
    role: str
    allowlist: frozenset[str]
    budget: Budget
    stop_on_tool_error: bool
    require_evidence: bool
    treat_tool_output_as_data: bool
    allow_dynamic_tools: bool
    trace_record_fields: tuple[str, ...]
    trace_forbidden_fields: tuple[str, ...]
    retention_days: int


@dataclass(frozen=True)
class Step:
    index: int
    tool: str
    argument_keys: tuple[str, ...]
    argument_fingerprint: str
    row_count: int
    source: str
    elapsed_ms: float
    outcome: str
    instruction_like_content: bool = False


@dataclass
class AgentRun:
    question: str
    role: str
    policy_id: str
    steps: list[Step] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    evidence: list[dict] = field(default_factory=list)
    answered: bool = False
    refused: bool = False
    stop_reason: str = ""
    elapsed_ms: float = 0.0
    answer: str = ""

    def as_trace(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "role": self.role,
            "steps": [asdict(step) for step in self.steps],
            "tools_used": self.tools_used,
            "evidence": self.evidence,
            "answered": self.answered,
            "refused": self.refused,
            "stop_reason": self.stop_reason,
            "elapsed_ms": round(self.elapsed_ms, 2),
        }


def load_policy(path: Path | str = Path(__file__).with_name("policy.yaml")) -> Policy:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    execution = raw["execution"]
    budget = raw["budget"]
    if execution.get("allow_dynamic_tools", False):
        raise ValueError("Politique refusée : l'ajout dynamique d'outils est interdit en M6.")
    if budget["max_steps"] > HARD_MAX_STEPS:
        raise ValueError(f"Politique refusée : max_steps au-delà de {HARD_MAX_STEPS}.")
    if budget["max_duration_ms"] > HARD_MAX_DURATION_MS:
        raise ValueError(f"Politique refusée : max_duration_ms au-delà de {HARD_MAX_DURATION_MS}.")
    if not raw["allowlist"]:
        raise ValueError("Politique refusée : liste blanche vide.")
    trace = raw["trace"]
    return Policy(
        policy_id=raw["policy_id"],
        role=raw["role"],
        allowlist=frozenset(raw["allowlist"]),
        budget=Budget(
            max_steps=int(budget["max_steps"]),
            max_tool_calls=int(budget["max_tool_calls"]),
            max_duration_ms=int(budget["max_duration_ms"]),
            max_repeated_calls=int(budget["max_repeated_calls"]),
            max_result_rows=int(budget["max_result_rows"]),
        ),
        stop_on_tool_error=bool(execution["stop_on_tool_error"]),
        require_evidence=bool(execution["require_evidence"]),
        treat_tool_output_as_data=bool(execution["treat_tool_output_as_data"]),
        allow_dynamic_tools=False,
        trace_record_fields=tuple(trace["record_fields"]),
        trace_forbidden_fields=tuple(trace["forbidden_fields"]),
        retention_days=int(trace["retention_days"]),
    )


def _fingerprint(arguments: dict) -> str:
    payload = json.dumps(arguments, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def _normalize(text: str) -> str:
    return (
        text.lower()
        .replace("é", "e").replace("è", "e").replace("ê", "e")
        .replace("à", "a").replace("â", "a")
        .replace("ù", "u").replace("û", "u")
        .replace("ô", "o").replace("î", "i").replace("ï", "i")
        .replace("ç", "c")
    )


def _question_has_instruction(question: str) -> bool:
    lowered = _normalize(question)
    return any(_normalize(marker) in lowered for marker in INSTRUCTION_MARKERS)


def _is_data_access_question(question: str) -> bool:
    lowered = _normalize(question)
    return any(_normalize(marker) in lowered for marker in DATA_ACCESS_MARKERS)


def _asks_definite_absence(question: str) -> bool:
    lowered = _normalize(question)
    return any(_normalize(marker) in lowered for marker in DEFINITE_ABSENCE_MARKERS)


def _asks_usage_name_without_inventory_id(question: str) -> bool:
    """True si la question vise un équipement via nom d'usage, sans EQ-… ni RPT-….

    Couvre le feedback actionnable (ambiguïté P-204 / pompe du nord) : refus
    avant planification, y compris si un LLM tenterait d'inventer un ID.
    """
    if EQUIPMENT_PATTERN.search(question) or REPORT_PATTERN.search(question):
        return False
    if USAGE_ALIAS_PATTERN.search(question):
        return True
    lowered = _normalize(question)
    attribute_markers = (
        "criticite", "site de l", "site de la", "fiche de", "fiche d",
    )
    equipment_nouns = (
        "pompe", "ventilateur", "vanne", "convoyeur", "equipement",
    )
    has_attribute = any(marker in lowered for marker in attribute_markers)
    has_noun = any(noun in lowered for noun in equipment_nouns)
    return has_attribute and has_noun


def _invented_equipment_id(tool: str, arguments: dict, question: str, state: dict) -> bool:
    """Refuse un equipment_id non issu de la question ni d'un outil précédent."""
    if tool not in EQUIPMENT_TOOLS:
        return False
    proposed = arguments.get("equipment_id")
    if not proposed:
        return True
    known = state.get("equipment_id")
    if known:
        return proposed != known
    return EQUIPMENT_PATTERN.search(question) is None


def _looks_like_instruction(result: ToolResult) -> bool:
    joined = " ".join(
        str(value) for row in result.rows for value in row.values()
    ).lower()
    return any(marker in joined for marker in INSTRUCTION_MARKERS)


class BoundedAgent:
    """Agent à étapes bornées, sans mémoire persistante ni effet externe."""

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        policy: Policy | None = None,
        planner: Planner | None = None,
    ) -> None:
        self.registry = registry or default_registry()
        self.policy = policy or load_policy()
        self.planner = planner or build_planner()
        unknown = sorted(self.policy.allowlist - set(self.registry.names()))
        if unknown:
            raise ValueError(f"Liste blanche incohérente avec le registre : {unknown}")

    def plan_next(self, question: str, state: dict) -> tuple[str, dict] | None:
        """Délègue au planificateur. La liste blanche est appliquée dans run()."""
        suggestion = self.planner.suggest(question, state, self.policy.allowlist)
        if suggestion is None:
            return None
        if not isinstance(suggestion, ToolPlan):
            return None
        return suggestion.tool, dict(suggestion.arguments)

    def run(self, question: str, *, faults: dict | None = None) -> AgentRun:
        run = AgentRun(question=question, role=self.policy.role, policy_id=self.policy.policy_id)
        # SCN-013 / ADV-001 : refuser AVANT tout appel si la question porte une instruction.
        if _question_has_instruction(question):
            run.refused = True
            run.stop_reason = "instruction_dans_question"
            run.answer = "Refus : la question contient une instruction hors politique."
            return run

        # SCN-009 / SCN-019 / FBK ambiguïté : nom d'usage ≠ inventaire.
        if _asks_usage_name_without_inventory_id(question):
            run.refused = True
            run.stop_reason = "identifiant_usage"
            run.answer = (
                "Refus : identifiant d'inventaire EQ-… requis ; "
                "un nom d'usage ne permet pas d'interroger la fiche."
            )
            return run

        state: dict[str, Any] = {
            "tools_used": [],
            "equipment_id": _first(EQUIPMENT_PATTERN, question),
            "report_id": _first(REPORT_PATTERN, question),
            "calls": {},
        }
        started = time.perf_counter()
        budget = self.policy.budget

        while True:
            elapsed = (time.perf_counter() - started) * 1000
            if elapsed > budget.max_duration_ms:
                run.stop_reason = "budget_duree_depasse"
                break
            if len(run.steps) >= budget.max_steps or len(run.steps) >= budget.max_tool_calls:
                run.stop_reason = "budget_etapes_depasse"
                break

            plan = self.plan_next(question, state)
            if plan is None:
                break
            tool, arguments = plan
            if tool not in self.policy.allowlist:
                run.stop_reason = "outil_hors_liste"
                break
            # Même axe : un planificateur LLM ne peut pas inventer un EQ-….
            if _invented_equipment_id(tool, arguments, question, state):
                run.stop_reason = "identifiant_invente"
                break

            fingerprint = _fingerprint({"tool": tool, **arguments})
            state["calls"][fingerprint] = state["calls"].get(fingerprint, 0) + 1
            if state["calls"][fingerprint] > budget.max_repeated_calls:
                run.stop_reason = "appel_repete"
                break

            try:
                result, elapsed_ms = self.registry.call(
                    tool, arguments, role=self.policy.role, faults=faults
                )
            except (ToolError, ArgumentError, AuthorizationError, UnknownTool) as exc:
                run.steps.append(Step(
                    index=len(run.steps) + 1, tool=tool,
                    argument_keys=tuple(sorted(arguments)),
                    argument_fingerprint=fingerprint,
                    row_count=0, source="", elapsed_ms=0.0,
                    outcome=type(exc).__name__,
                ))
                state["tools_used"].append(tool)
                run.tools_used.append(tool)
                if self.policy.stop_on_tool_error:
                    run.stop_reason = "erreur_outil"
                    break
                continue

            instruction_like = _looks_like_instruction(result)
            run.steps.append(Step(
                index=len(run.steps) + 1, tool=tool,
                argument_keys=tuple(sorted(arguments)),
                argument_fingerprint=fingerprint,
                row_count=len(result.rows), source=result.source,
                elapsed_ms=round(elapsed_ms, 2),
                outcome="vide" if result.empty else "ok",
                instruction_like_content=instruction_like,
            ))
            state["tools_used"].append(tool)
            run.tools_used.append(tool)
            # Contenu récupéré = donnée : on signale mais on n'exécute pas l'instruction.
            if instruction_like and self.policy.treat_tool_output_as_data:
                pass
            self._collect_evidence(tool, result, run, state)

        run.elapsed_ms = (time.perf_counter() - started) * 1000
        self._conclude(run)
        return run

    def _collect_evidence(self, tool: str, result: ToolResult, run: AgentRun, state: dict) -> None:
        for row in result.rows:
            if tool == "search_knowledge":
                run.evidence.append({
                    "type": "document",
                    "reference": row["document_id"],
                    "revision": row["revision"],
                })
            elif tool == "diagnose_report":
                if row.get("equipment_id"):
                    state["equipment_id"] = row["equipment_id"]
                run.evidence.append({"type": "rapport", "reference": row["report_id"]})
            else:
                key = next(
                    (name for name in ("event_id", "maintenance_id", "equipment_id") if name in row),
                    None,
                )
                run.evidence.append({
                    "type": "enregistrement",
                    "reference": row.get(key, tool),
                    "source": result.source,
                })

    def _conclude(self, run: AgentRun) -> None:
        if run.stop_reason:
            run.refused = True
            run.answer = f"Refus : {run.stop_reason}."
            return

        references = {item["reference"] for item in run.evidence}

        # SCN-014 : politique d'accès — le document restreint doit être présent ;
        # sinon refus après l'appel (filtrage rôle déjà fait dans l'outil).
        if _is_data_access_question(run.question) and "DOC-DATA-ACCESS-001" not in references:
            run.refused = True
            run.stop_reason = "acces_refuse"
            run.answer = "Refus : document d'accès non admissible pour ce rôle."
            return

        # SCN-020 : absence d'événement ≠ preuve d'absence de défaut.
        if _asks_definite_absence(run.question):
            run.refused = True
            run.stop_reason = "preuve_insuffisante"
            run.answer = (
                "Refus : une liste d'événements ne permet pas d'affirmer "
                "l'absence de défaut."
            )
            return

        if self.policy.require_evidence and not run.evidence:
            run.refused = True
            run.stop_reason = "preuve_insuffisante"
            run.answer = "Refus : aucune preuve admissible n'a été obtenue."
            return

        run.answered = True
        run.stop_reason = "reponse_produite"
        run.answer = f"Réponse fondée sur : {', '.join(sorted(references))}."


def _first(pattern: re.Pattern[str], text: str) -> str | None:
    found = pattern.search(text)
    return found.group(0) if found else None
