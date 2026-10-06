"""Candidat : refus explicite nom d'usage / ID inventé."""

from __future__ import annotations

from dataclasses import replace

from agent.providers import HeuristicPlanner
from agent.registry import default_registry
from agent.runner import BoundedAgent, load_policy


def _agent() -> BoundedAgent:
    return BoundedAgent(default_registry(), load_policy(), HeuristicPlanner())


def test_scn009_refus_nom_usage_avant_appel():
    agent = BoundedAgent(
        default_registry(),
        replace(load_policy(), role="technicien"),
        HeuristicPlanner(),
    )
    run = agent.run("Quelle est la criticité de la pompe P-204 ?")
    assert run.refused
    assert run.stop_reason == "identifiant_usage"
    assert not run.tools_used


def test_scn019_refus_ambiguite_avant_appel():
    agent = _agent()
    run = agent.run(
        "Quelle est la criticité de la pompe du nord, celle qu'on appelle parfois P-204 ?"
    )
    assert run.refused
    assert run.stop_reason == "identifiant_usage"
    assert not run.tools_used


def test_eq_explicite_non_bloque():
    agent = _agent()
    run = agent.run("Quelle est la criticité et le site de l'équipement EQ-PUMP-001 ?")
    assert run.answered
    assert "get_equipment" in run.tools_used


def test_procedure_pompe_sans_alias_reste_documentaire():
    """SCN-011 : procédure générique — ne pas confondre avec un nom d'usage."""
    agent = _agent()
    run = agent.run(
        "Quelle procédure s'applique à une vibration de pompe hors seuil ?",
        faults={"search_knowledge": {"error": "unavailable"}},
    )
    assert run.refused
    assert run.stop_reason == "erreur_outil"
    assert "search_knowledge" in run.tools_used


def test_planificateur_invente_refuse():
    class InventingPlanner:
        def suggest(self, question, state, allowlist):
            from agent.providers import ToolPlan
            return ToolPlan("get_equipment", {"equipment_id": "EQ-PUMP-001"})

    agent = BoundedAgent(default_registry(), load_policy(), InventingPlanner())
    # Pas d'alias P-… ni couple attribut+nom : le garde-fou plan doit trancher.
    run = agent.run("Donne le détail pour cet appareil anonyme du hall B.")
    assert run.refused
    assert run.stop_reason == "identifiant_invente"
    assert not run.tools_used
