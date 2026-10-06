<div align="center">

# DiagOps M4 — Modèle · RAG · Agent

**Classifieur · retrieval lexical/vectoriel · agent une action (lecture seule)**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Stack](https://img.shields.io/badge/sklearn_+_RAG-0f766e?style=flat-square)](#carte)
[![Décision](https://img.shields.io/badge/décision-adopter_sous_conditions-059669?style=flat-square)](docs/matrice_decision.md)

</div>

---

## Objectif

Concevoir une chaîne **modèle + retrieval + agent borné** : citations, abstention,  
menaces documentées — sans effet externe, sans régler sur le test scellé.

## Statut

| Champ | Valeur |
|-------|--------|
| Décision | **Adopter sous conditions** ([matrice](docs/matrice_decision.md)) |
| Preuve clé | [`docs/`](docs/) · [`journal_bord.md`](journal_bord.md) |
| Suite | [M5](../M5/) |

## Démarrage

```bash
cd work/M4
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.lock
python3 -m pytest -q
```

```bash
python3 launch.py --help
python3 scripts/run_pipeline.py --help
```

## Données

```text
../../data_pack/2026-S1/model_eval/sensor_calibration.csv
../../data_pack/2026-S1/knowledge/manifest.csv
../../data_pack/2026-S1/knowledge/documents/
../../data_pack/2026-S1/rag_eval/questions.jsonl
../../data_pack/2026-S1/reference_runs/m3_for_m4/
```

> Les jeux `test` scellés restent côté formateur.

## Carte

```text
M4/
├── configs/       # model, retrieval
├── src/           # rag, agent, threats, brief2
├── docs/          # conception, benchmarks, passage M5
├── scripts/
├── tests/
├── veille_diagops/
└── notebooks/
```

## Vérifier

```bash
python3 -m pytest -q
```

## Preuves

| Document | Contenu |
|----------|---------|
| [docs/matrice_decision.md](docs/matrice_decision.md) | Décision |
| [docs/protocole_evaluation.md](docs/protocole_evaluation.md) | Protocole |
| [docs/threat_model.md](docs/threat_model.md) | Menaces |
| [docs/passage_m5.md](docs/passage_m5.md) | Relais M5 |
| [veille_diagops/](veille_diagops/) | Veille |

## Suite

→ [M5 — Déploiement & observabilité](../M5/)

---

<div align="center"><sub>DiagOps S04 · work/M4 · README unifié</sub></div>
