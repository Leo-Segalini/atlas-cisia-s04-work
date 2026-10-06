<div align="center">

# DiagOps M5 — Déployer & observer

**Index atomique · gates · Compose · rollback · game day**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Stack](https://img.shields.io/badge/FastAPI_+_Docker-0f766e?style=flat-square)](#carte)
[![Guide](https://img.shields.io/badge/guide-HTML_schémas-7c3aed?style=flat-square)](docs/comprendre_m5.html)

</div>

---

## Objectif

Passer d’un candidat M4 à une **release contrôlée** : construction d’index,  
évaluation de gates, promotion réversible, runbook et exercice de crise.

## Statut

| Champ | Valeur |
|-------|--------|
| Exercice rollback | Documenté ([rapport](docs/rapport_rollback.md)) |
| Preuve clé | [`docs/`](docs/) · [`game_day/`](game_day/) · [`pipelines/`](pipelines/) |
| Suite | [M6](../M6/) |

## Démarrage

```bash
cd work/M5
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.lock
python3 -m pytest -q
```

Index candidat (exemple) :

```bash
python3 pipelines/build_index.py \
  --manifest ../../data_pack/2026-S1/knowledge/manifest.csv \
  --documents ../../data_pack/2026-S1/knowledge/documents \
  --output artifacts/candidates/local/index.json
```

## Données / référence

```text
../../data_pack/2026-S1/knowledge/
../../data_pack/2026-S1/reference_runs/m4_for_m5/
```

## Carte

```text
M5/
├── src/app.py           # API instrumentée
├── pipelines/           # build, evaluate, promote, rollback, CI local
├── deploy/              # Dockerfile, Compose, Prometheus
├── configs/gates.json
├── docs/                # runbook, rollback, guide HTML
├── game_day/
└── monitoring/
```

## Vérifier

```bash
python3 -m pytest -q
bash pipelines/ci_local.sh    # si environnement prêt
```

## Preuves

| Document | Contenu |
|----------|---------|
| [docs/comprendre_m5.html](docs/comprendre_m5.html) | Guide visuel |
| [docs/runbook.md](docs/runbook.md) | Exploitation |
| [docs/rapport_rollback.md](docs/rapport_rollback.md) | Restauration |
| [game_day/](game_day/) | Jour J / défense |
| [veille_diagops/passage_m6.md](veille_diagops/passage_m6.md) | Relais M6 |

## Suite

→ [M6 — Agent, feedback, campagne](../M6/)

---

<div align="center"><sub>DiagOps S04 · work/M5 · README unifié</sub></div>
