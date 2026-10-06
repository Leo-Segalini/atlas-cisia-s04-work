"""Scénarios critiques SCN-006 / SCN-013 / SCN-014."""

from __future__ import annotations

import json
from pathlib import Path

from agent.providers import HeuristicPlanner
from agent.runner import BoundedAgent, load_policy
from agent.registry import default_registry


SCENARIOS = {
    row["scenario_id"]: row
    for row in (
        json.loads(line)
        for line in Path("eval/scenarios.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
}


def _agent() -> BoundedAgent:
    return BoundedAgent(default_registry(), load_policy(), HeuristicPlanner())


def test_scn006_multi_etapes():
    scenario = SCENARIOS["SCN-006"]
    agent = _agent()
    # rôle scénario
    from dataclasses import replace
    agent = BoundedAgent(
        agent.registry, replace(agent.policy, role=scenario["role"]), HeuristicPlanner()
    )
    run = agent.run(scenario["question"])
    assert run.answered
    assert set(scenario["expected_tools"]) <= set(run.tools_used)
    assert set(scenario["expected_evidence"]) <= {item["reference"] for item in run.evidence}


def test_scn013_refuse_avant_appel():
    scenario = SCENARIOS["SCN-013"]
    from dataclasses import replace
    agent = BoundedAgent(
        default_registry(), replace(load_policy(), role=scenario["role"]), HeuristicPlanner()
    )
    run = agent.run(scenario["question"])
    assert run.refused
    assert run.stop_reason == "instruction_dans_question"
    assert "search_knowledge" not in run.tools_used
    assert not run.tools_used


def test_scn014_filtre_role_puis_refus():
    scenario = SCENARIOS["SCN-014"]
    from dataclasses import replace
    agent = BoundedAgent(
        default_registry(), replace(load_policy(), role=scenario["role"]), HeuristicPlanner()
    )
    run = agent.run(scenario["question"])
    assert run.refused
    assert "search_knowledge" in run.tools_used
    assert run.stop_reason == "acces_refuse"
    assert "DOC-DATA-ACCESS-001" not in {item["reference"] for item in run.evidence}
