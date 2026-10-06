<div align="center">

# DiagOps M6 — Agent borné & feedback

**Outils lecture seule · scénarios gelés · candidat · campagne adversariale**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Politique](https://img.shields.io/badge/policy-m6--candidat--ambiguite--r1-7c3aed?style=flat-square)](agent/policy.yaml)
[![Décision](https://img.shields.io/badge/décision-prolonger-d97706?style=flat-square)](docs/decision_promotion.md)

</div>

---

## Objectif

Outiller un agent **mono-acteur borné** (5 outils RO), qualifier le feedback  
humain, tester **une** hypothèse, résister à une campagne — sans effet externe.

## Statut

| Champ | Valeur |
|-------|--------|
| Politique | `m6-candidat-ambiguite-r1` |
| Gel scénarios | sha256 `29fa0c7b…cd04e7` (24 cas) |
| Gel / campagne | réussite **1,0** · interdits **0** |
| Décision | **`prolonger`** — [decision_promotion.md](docs/decision_promotion.md) |
| Suite | [M7](../M7/) |

## Démarrage

```bash
cd work/M6
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.lock
python3 -m pytest -q
```

## Données

```text
../../data_pack/2026-S1/reference_runs/m5_for_m6/
../../data_pack/2026-S1/knowledge/
../../data_pack/2026-S1/equipment/equipment.csv
../../data_pack/2026-S1/events/events.csv
../../data_pack/2026-S1/maintenance/maintenance_history.csv
../../data_pack/2027-S1/reports/reports.jsonl
../../data_pack/2027-S1/feedback/feedback.csv
```

## Carte

```text
M6/
├── agent/           # policy, runner, registry, planners
├── tools/           # 5 adaptateurs RO
├── eval/            # harness + scenarios_gel
├── feedback/        # qualification (pas de labels auto)
├── adversarial/     # campagne, invariants, défense
├── docs/            # registre, politique, online, décision
├── results/         # preuves de mesure
└── veille_diagops/  # passage M7
```

## Vérifier

```bash
python3 -m pytest -q

python3 eval/run_agent_eval.py \
  --scenarios eval/scenarios_gel.jsonl \
  --output results/eval_scenarios_gel.json

python3 feedback/qualify_feedback.py --batch all \
  --output results/feedback_b1_b2.json

python3 eval/run_agent_eval.py \
  --scenarios adversarial/campaign.jsonl \
  --output results/campagne_apres.json
```

Planificateur (défaut **heuristic**) :

```bash
export DIAGOPS_PLANNER=heuristic   # ollama | huggingface en option labo
```

## Preuves

| Document | Contenu |
|----------|---------|
| [docs/rapport_evaluation.md](docs/rapport_evaluation.md) | Mesures gel |
| [docs/qualification_feedback.md](docs/qualification_feedback.md) | Classes feedback |
| [docs/hypothese_candidat.md](docs/hypothese_candidat.md) | Axe unique |
| [docs/decision_promotion.md](docs/decision_promotion.md) | Prolonger |
| [adversarial/report.md](adversarial/report.md) | Campagne |
| [results/candidat/](results/candidat/) | Config + évals |
| [veille_diagops/passage_m7.md](veille_diagops/passage_m7.md) | Relais |

## Suite

→ [M7 — Architecture & réversibilité](../M7/)

---

<div align="center"><sub>DiagOps S04 · work/M6 · README unifié</sub></div>
