# Rapport de dérive — brief online M6

**Date :** 2026-09-21  
**Version active (référence) :** `diagops-m5-reference-r1` (`data_pack/2026-S1/reference_runs/m5_for_m6/`)  
**Candidat labo agent :** `m6-candidat-ambiguite-r1` (après remédiation ADV-003)

## Version active — cadrage

| Élément | Valeur |
|---|---|
| Release | `diagops-m5-reference-r1` |
| Environnement | préproduction pédagogique locale (Compose M5) |
| Calibration | `evaluation/metrics_calibration.json` — `test_split_used: false` |
| Gates | `gates/gates.json` (citation ≥ 1,0 ; abstention ≥ 1,0 ; docs ≥ 7 ; hit@3 ≥ 0,8) |
| Agent M5 | 1 étape max (`maximum_agent_steps: 1`) |
| Rollback | `operations/restauration.md` |

## Limites assumées de la référence

- données et procédures **synthétiques** ;
- pas de démonstration industrielle ni conformité réglementaire tranchée ;
- pas d'outil à effet externe ;
- promotion **humaine** uniquement.

## Ce qui change avec `2027-S1`

| Dimension | 2026-S1 (référence) | 2027-S1 (nouvelles données) | Lecture dérive |
|---|---|---|---|
| Rapports | 40 | 60 (+50 %) | volume ↑, charge diagnostic ↑ |
| Schéma `reports.jsonl` | 7 champs identiques | identique | **pas de rupture de contrat** |
| Canaux | mobile_app, web_form, radio | + **sms_gateway** (18) | canal court / bruit ↑ |
| `event_id` null | 0 | **54 / 60** | lien événement souvent absent |
| Longueur note (moy.) | ~177 car. | ~91 car. | SMS / notes tronquées |
| Feedback | — | 124 retours (b1+b2) | nouveau signal, **pas labels** |
| Agent M6 | — | 5 outils lecture, multi-étapes bornées | périmètre outillage ↑ |

## Hypothèse testée (rappel T6)

Une seule modification : refus explicite des noms d'usage / IDs inventés.  
Mécanisme : `identifiant_usage` avant plan + `identifiant_invente` avant appel.

## Décision liée

Voir `docs/decision_promotion.md` et `docs/online/plan_deploiement.md` : **prolonger** tant que la campagne et la supervision humaine n'ont pas tranché une activation.
