<div align="center">

# DiagOps M3 — Multisource & base de données

**Capteurs · règles · quarantaine unifiée · SQLAlchemy**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Stack](https://img.shields.io/badge/SQLAlchemy_+_Alembic-0f766e?style=flat-square)](#carte)
[![Handoff](https://img.shields.io/badge/handoff-M4-64748b?style=flat-square)](docs/decision_transmission_m4.md)

</div>

---

## Objectif

Intégrer **quatre sources**, appliquer un registre de règles, persister proprement  
et transmettre un jeu qualifié vers M4 (sans inventer les anomalies formateur).

## Statut

| Champ | Valeur |
|-------|--------|
| Livrable | BDD + docs + notebooks + UI explorer |
| Preuve clé | [`docs/decision_transmission_m4.md`](docs/decision_transmission_m4.md) |
| Suite | [M4](../M4/) |

## Démarrage

```bash
cd work/M3
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.lock
python3 -m pytest -q
```

## Données

Sources ouvertes sous `../../data_pack/2026-S1/` (équipements, événements,  
maintenance, capteurs — détail dans le brief et `docs/`).

Sorties locales : `output/` (processed, audit, brief2).

## Carte

```text
M3/
├── docs/          # décisions, flux, couverture
├── output/        # CSV / DB de travail
├── notebooks/
├── ui/            # explorateur
├── tests/
└── journal_bord.md
```

## Vérifier

```bash
python3 -m pytest -q
# UI optionnelle selon README_TRAVAIL
```

## Preuves

| Chemin | Contenu |
|--------|---------|
| [docs/](docs/) | Diagnostic, flux, transmission M4 |
| [journal_bord.md](journal_bord.md) | Chronologie |
| [README_TRAVAIL.md](README_TRAVAIL.md) | Notes opérationnelles |

## Suite

→ [M4 — Modèle, RAG, agent](../M4/)

---

<div align="center"><sub>DiagOps S04 · work/M3 · README unifié</sub></div>
