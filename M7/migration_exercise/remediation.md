# Remédiation et défense — brief 2

**Date :** 2026-10-06

## Traitement des constats

| ID | Action | Statut |
|---|---|---|
| IR-01 | Décision cible = différer ; case ouverte pour signature formateur | ouvert process |
| IR-02 | Fallback heuristic documenté ; pas de promo cloud | clos labo |
| IR-03 | Clarifié dans execution_log + residual_risks | clos |
| IR-04 | Limitations lab report citées | clos |
| IR-05 | ADR-0002 + gates target | clos (blocage volontaire) |

## Rejeu

`python migration_exercise/run_personal.py` → status **passed** (dossier déjà présent : ne pas écraser ; preuve `results/migration-brief2-r1/report.json`).  
`python -m unittest discover -s tests -v` → OK.

## Défense de la cible

Maintenir JSON actif + SQLite candidat est défendable : réversibilité prouvée, ACL avant score, zéro effet réel.  
Argument opposé (« migrer tout de suite vers SQLite/cloud ») écarté faute de signature tierce et de panne fournisseur réelle.
