<div align="center">

# DiagOps M7 — Architecture & réversibilité

**Cartographie · menaces · portabilité JSON→SQLite · outil simulé · veille**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Deps](https://img.shields.io/badge/deps-stdlib_only-0f766e?style=flat-square)](#démarrage)
[![Décision](https://img.shields.io/badge/cible-différer-ea580c?style=flat-square)](architecture/target.md)

</div>

---

## Objectif

Challenger l’architecture RAG-agentique : frontières de confiance, migration  
réversible d’index, red team locale, spécification d’un **outil à effet simulé**  
(hors chemin de référence). Aucun service payant requis.

## Statut

| Champ | Valeur |
|-------|--------|
| Lab discovery | `results/decouverte-r1` — **passed** (hit@3 = 1,0) |
| Migration brief 2 | `results/migration-brief2-r1` — **passed** |
| Cible | **Différer** effets réels & bascule d’index actif |
| Revue formateur | Signature externe **pending** |
| Suite | [handoff M8](handoff_m8.md) |

## Démarrage

Aucun `pip` obligatoire.

```bash
cd work/M7
python3 -m unittest discover -s tests -v
python3 lab.py --output results/decouverte-r1
python3 migration_exercise/run_personal.py --output results/migration-brief2-r1
```

> Chaque `--output` doit être un **nouveau** dossier (refus d’écrasement).

## Données

```text
../../data_pack/2026-S1/knowledge/
../../data_pack/2026-S1/rag_eval/questions.jsonl
../../data_pack/2026-S1/reference_runs/m6_for_m7/   # limites starter M6
```

État personnel M6 (si présent) : `../M6/` — ne pas mélanger avec la référence  
commune dans une même comparaison.

## Carte

```text
M7/
├── architecture/     # current, target, ADR
├── security/         # threats, red team, data policy
├── portability/      # alternatives, exercice
├── resilience/       # scénarios, RTO/RPO labo
├── simulated_action/ # contrat non exécutable
├── migration_exercise/
├── online/           # brief online autonome
├── veille_diagops/
├── lab.py
└── results/
```

## Vérifier

```bash
python3 -m unittest discover -s tests -v
# Lire results/*/report.json — status doit être "passed"
```

## Preuves

| Document | Contenu |
|----------|---------|
| [architecture/current.md](architecture/current.md) | Cartographie |
| [architecture/target.md](architecture/target.md) | Cible + gates |
| [architecture/adr/0001-modele.md](architecture/adr/0001-modele.md) | Index JSON/SQLite |
| [architecture/adr/0002-outil-simule.md](architecture/adr/0002-outil-simule.md) | Effet simulé |
| [security/](security/) | Menaces & risques résiduels |
| [migration_exercise/](migration_exercise/) | Contrat, revue, remédiation |
| [online/dossier.md](online/dossier.md) | Brief online |
| [handoff_m8.md](handoff_m8.md) | Questions ouvertes |

## Suite

→ Préparer **M8** à partir de [`handoff_m8.md`](handoff_m8.md)  
(référence commune M8 ≠ ce dépôt).

---

<div align="center"><sub>DiagOps S04 · work/M7 · README unifié</sub></div>
