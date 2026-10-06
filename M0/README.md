<div align="center">

# DiagOps M0 — Intégration modèle

**API de diagnostic · Hugging Face Inference · UI Streamlit / HTML**

[![Python](https://img.shields.io/badge/python-3.11+-1d4ed8?style=flat-square)](#démarrage)
[![Stack](https://img.shields.io/badge/FastAPI_+_Pydantic-0f766e?style=flat-square)](#carte)
[![Suite](https://img.shields.io/badge/suite-M1-64748b?style=flat-square)](../M1/)

</div>

---

## Objectif

Exposer un assistant de diagnostic maintenance **sans fine-tuning** :  
`POST /diagnose` + interface opérateur, modèle sur étagère (HF ou baseline locale).

## Statut

| Champ | Valeur |
|-------|--------|
| Livrable | API + UI + tests + notebook |
| Preuve clé | [`evaluation_m0.md`](evaluation_m0.md) · [`notebooks/`](notebooks/) |
| Suite | [M1 — LoRA](../M1/) |

## Démarrage

```bash
cd work/M0
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env   # renseigner HF_TOKEN si mode cloud
```

| Variable | Rôle |
|----------|------|
| `HF_TOKEN` | Inference API (ne jamais committer) |
| `HF_MODEL` | ex. `Qwen/Qwen2.5-7B-Instruct` |
| `DIAGOPS_API_URL` | URL client UI (défaut `http://127.0.0.1:8000`) |

## Données

```text
../../data_pack/2026-S1/reports/reports.jsonl
```

## Carte

```text
M0/
├── app/           # FastAPI, schémas, client modèle
├── ui/            # Streamlit + page HTML
├── tests/
├── notebooks/
└── .env.example
```

## Vérifier

```bash
python3 -m pytest -q
uvicorn app.main:app --reload --port 8000
streamlit run ui/streamlit_app.py
```

## Preuves

| Document | Contenu |
|----------|---------|
| [evaluation_m0.md](evaluation_m0.md) | Évaluation intégration |
| [notebooks/m0_integration_diagops.ipynb](notebooks/m0_integration_diagops.ipynb) | Synthèse |

## Suite

→ [M1 — Fine-tuning LoRA](../M1/)

---

<div align="center"><sub>DiagOps S04 · work/M0 · README unifié</sub></div>
