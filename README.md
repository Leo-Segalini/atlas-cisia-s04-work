# DiagOps S04 — Rendu `work/`

Export **public** du travail apprenant Atlas CISIA S04 (modules M0 → M7).

Ce dépôt contient uniquement le dossier de production `work/` (modules à la racine : `M0/` … `M7/`).  
Il n’inclut **pas** le data pack formateur, ni les briefs, ni les secrets.

## Contenu

| Module | Contenu principal |
|---|---|
| M0–M5 | Travaux et preuves des modules précédents |
| M6 | Agent borné, feedback, candidat, campagne, veille → M7 |
| M7 | Revue d’architecture, portabilité JSON→SQLite, migration, handoff M8 |

## Exclusions volontaires (non publiées)

- environnements `.venv/`
- fichiers `.env` (tokens) — seuls les `.env.example` sont présents
- caches Python
- index locaux reconstruisibles (`corpus.json`, `index.sqlite`)
- checkpoints lourds `optimizer.pt`

## Reproduction indicative

Les données restent dans le data pack pédagogique du dépôt S04 (non fourni ici).  
Voir les `README.md` de chaque module pour les commandes (`pytest`, `lab.py`, etc.).

## Décisions clés

- M6 : candidat `m6-candidat-ambiguite-r1`, décision **`prolonger`**
- M7 : architecture cible **`différer`** (pas d’outil à effet réel ; index JSON actif)

---

Rendu pédagogique — pas un produit industriel.
