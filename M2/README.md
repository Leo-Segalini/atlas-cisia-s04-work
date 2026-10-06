<div align="center">

# DiagOps M2 — Qualité & pipeline données

**Validation · quarantaine · statistiques · PII**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Stack](https://img.shields.io/badge/pandas_+_validation-0f766e?style=flat-square)](#carte)
[![CI](https://img.shields.io/badge/CI-workflow_M2-64748b?style=flat-square)](.github/workflows/m2-qualification.yml)

</div>

---

## Objectif

Charger les tables maintenance, **qualifier** les anomalies, isoler en quarantaine  
et produire un audit statistique défendable avant la suite multisource (M3).

## Statut

| Champ | Valeur |
|-------|--------|
| Livrable | Pipeline + rapports + notebooks |
| Preuve clé | [`journal_bord.md`](journal_bord.md) · [`reports/`](reports/) · [`output/`](output/) |
| Suite | [M3](../M3/) |

## Démarrage

```bash
cd work/M2
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.lock
python3 -m pytest -q
```

## Données

```text
../../data_pack/2026-S1/equipment/equipment.csv
../../data_pack/2026-S1/events/events.csv
../../data_pack/2026-S1/maintenance/maintenance_history.csv
```

## Carte

```text
M2/
├── contracts/     # schémas
├── scripts/       # qualification / pipeline
├── output/        # processed, quarantine, reports JSON
├── reports/       # audit, figures, HTML
├── notebooks/
└── aller_plus_loin/
```

## Vérifier

```bash
python3 -m pytest -q
python3 launch.py --help
```

## Preuves

| Chemin | Contenu |
|--------|---------|
| [reports/audit_report.md](reports/audit_report.md) | Audit |
| [output/validation_report.json](output/validation_report.json) | Validation |
| [journal_bord.md](journal_bord.md) | Décisions |
| [README_TRAVAIL.md](README_TRAVAIL.md) | Notes |

## Suite

→ [M3 — Multisource & base de données](../M3/)

---

<div align="center"><sub>DiagOps S04 · work/M2 · README unifié</sub></div>
