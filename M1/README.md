<div align="center">

# DiagOps M1 — Fine-tuning LoRA

**Split reproductible · entraînement Qwen · métriques DiagOps**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Stack](https://img.shields.io/badge/Transformers_+_PEFT-0f766e?style=flat-square)](#carte)
[![Décision](https://img.shields.io/badge/décision-prolonger-d97706?style=flat-square)](#statut)

</div>

---

## Objectif

Comparer une **baseline** et un adaptateur **LoRA** sur la tâche de diagnostic,  
avec split, environnement et métriques figés — sans conclure trop tôt.

## Statut

| Champ | Valeur |
|-------|--------|
| Décision | **Prolonger** (smoke Mac / MPS) — voir preuves |
| Preuve clé | [`work/evidence/decision_m1.md`](work/evidence/decision_m1.md) |
| Modèle épinglé | révision HF documentée dans le kit (ne pas suivre `main`) |
| Suite | [M2](../M2/) |

## Démarrage

```bash
cd work/M1
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.lock
```

Configs : `configs/` (référence GPU) · `configs/mac_smoke/` (smoke local).

```bash
python3 launch.py --help   # selon protocole du module
python3 -m pytest -q
```

## Données

Annotations et splits via `data_pack/` (chemins dans les configs YAML).  
Artefacts locaux sous `work/` (predictions, adapter smoke, evidence).

## Carte

```text
M1/
├── configs/          # baseline, lora, variantes, mac_smoke
├── src/              # train, evaluate, metrics, dataset
├── templates/        # model card, peer review, protocol
├── notebooks/
├── work/             # runs, evidence, splits
└── tests/
```

## Vérifier

```bash
python3 -m pytest -q
# Consulter work/evidence/ et work/smoke_mac/*/metrics.json
```

## Preuves

| Chemin | Contenu |
|--------|---------|
| [work/evidence/](work/evidence/) | Décision, model card, peer review |
| [work/smoke_mac/](work/smoke_mac/) | Run smoke + adapter |
| [README_TRAVAIL.md](README_TRAVAIL.md) | Notes de travail |

## Suite

→ [M2 — Qualité des données](../M2/)

---

<div align="center"><sub>DiagOps S04 · work/M1 · README unifié</sub></div>
