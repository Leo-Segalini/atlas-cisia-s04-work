# Décision de promotion — candidat `m6-candidat-ambiguite-r1`

**Date :** 2026-09-21  
**Décideur :** apprenant M6 (labo)  
**Décision :** **`prolonger`**

## Une seule différence listée

| Élément | Référence `m6-baseline-r1` | Candidat `m6-candidat-ambiguite-r1` |
|---|---|---|
| Refus nom d'usage (SCN-009, SCN-019) | `preuve_insuffisante` après planification vide | `identifiant_usage` avant tout appel |
| Invention d'`EQ-…` par le planificateur | non bloquée explicitement | `identifiant_invente` |

Tout le reste (allowlist, budgets, outils, gel) est identique.

## Mesures agent (jeu gelé, 24 scénarios)

Empreinte gel : `sha256=29fa0c7bcbcf59ad5b2f7cf45f1c8a11a09ec26eb05c371811b69a7177cd04e7`

| Métrique | Baseline T4 (`eval_scenarios_gel.json`) | Candidat (`results/candidat/…`) |
|---|---:|---:|
| Réussite scénarios | 1,000 | 1,000 |
| Appels interdits | 0 | 0 |
| Refus incorrects | 0 | 0 |
| Refus corrects | 13 | 13 |
| Dépassements budget | 0 | 0 |

Aucune régression sur SCN-001…005 ni sur le reste du gel.

## Gates M5 (`m5_for_m6`) — rappel, non recalibrés

Le candidat **ne modifie pas** le pipeline RAG M5. Les gates de référence restent :

| Gate (`gates/gates.json`) | Seuil référence | Lecture M6 |
|---|---:|---|
| `minimum_citation_resolvable_rate` | 1,0 | inchangé (hors axe agent) |
| `minimum_correct_abstention_rate` | 1,0 | inchangé |
| `minimum_document_count` | 7 | inchangé |
| `minimum_expected_document_hit_at_3` | 0,8 | inchangé (mesure cal. = 1,0) |

Métriques calibration (`evaluation/metrics_calibration.json`) : `test_split_used: false` — **aucun réglage sur test scellé**.

## Rollback

Procédure citée : `data_pack/2026-S1/reference_runs/m5_for_m6/operations/restauration.md`  
Release saine : `diagops-m5-reference-r1`.  
Pour l'agent labo : revenir à `policy_id: m6-baseline-r1` et retirer les garde-fous `identifiant_usage` / `identifiant_invente` si besoin d'A/B.

## Pourquoi pas `promouvoir` maintenant

1. La campagne adversariale (T8 / INV-01…09) n'est **pas** encore rejouée sur ce candidat.
2. Le brief online (T7) n'a pas encore formalisé le plan de déploiement préprod→prod.
3. Un gain mesurable sur le gel est surtout **qualitatif** (motif de refus) ; la durcissement LLM sera prouvé sous attaque / provider non heuristique.

## Pourquoi pas `rejeter`

- zéro régression historique sur le gel ;
- hypothèse issue de feedback **actionnable** qualifié ;
- allowlist et absence d'effet respectées.

## Suite conditionnelle

`prolonger` jusqu'à :

1. campagne adversariale verte sur le candidat ;
2. décision humaine post-T8 sans invariant ouvert ;

alors seulement une nouvelle fiche pourra porter `promouvoir` (activation labo / préprod documentée), jamais une promotion automatique.


## Mise à jour post-T8

Campagne passée à 1,0 après remédiation ADV-003 ; **aucun invariant ouvert**. La décision reste **`prolonger`** (argument de défense : couverture adversariale encore étroite, supervision humaine — `adversarial/defense.md`).
