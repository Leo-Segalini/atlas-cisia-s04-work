# Métriques segmentées — online M6

**Source :** `results/candidat/eval_apres_remediation.json`  
**Jeu :** `eval/scenarios_gel.jsonl` (24) · politique `m6-candidat-ambiguite-r1`

## Par famille de catégories

| Famille | Catégories | n | Réussite |
|---|---|---:|---:|
| nominal | nominal_document, nominal_equipment, nominal_events, nominal_history, nominal_report, short_channel | 6 | 1,000 |
| multi_étapes | multi_step, multi_step_history, useless_tool | 3 | 1,000 |
| refus_identifiant | invalid_argument, identifiant_ambigu, unknown_id, unknown_report | 4 | 1,000 |
| dégradé / timeout | unavailable_tool, timeout, timeout_cascade, timeout_events, empty_result, preuve_insuffisante | 6 | 1,000 |
| sécurité / accès | injection_question, role_restriction, out_of_scope | 3 | 1,000 |
| contradiction | contradictory_sources, contradiction_structure_document | 2 | 1,000 |

## Synthèse globale

| Métrique | Valeur |
|---|---:|
| Réussite scénarios | 1,000 |
| Appels interdits | 0 |
| Refus incorrects | 0 |
| Refus corrects | 13 |
| Choix d'outil exact | 0,958 |
| Baseline sans agent | 0,083 |

## Campagne adversariale (segment sécurité)

| Jeu | Avant remédiation | Après |
|---|---:|---:|
| `adversarial/campaign.jsonl` (7 cas) | 0,857 (1 interdit) | **1,000** (0 interdit) |

Aucune régression segmentaire détectée sur le gel après correction ADV-003.
