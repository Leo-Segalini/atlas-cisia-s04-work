# Hypothèse candidat — M6

**Date :** 2026-09-21  
**Candidat :** `m6-candidat-ambiguite-r1`  
**Référence labo agent :** `m6-baseline-r1` (mesure gel T4)  
**Référence M5 restaurable :** `diagops-m5-reference-r1` (`data_pack/2026-S1/reference_runs/m5_for_m6/`)  
**Feedback source :** `FBK-2027S1-0001`, `FBK-2027S1-0004` (classe `actionnable`, qualification T5)

## Axe unique modifié

**Politique de refus — identifiant d'usage / inventaire inventé.**

Une seule différence fonctionnelle par rapport à `m6-baseline-r1` :

| Avant (baseline) | Après (candidat) |
|---|---|
| Nom d'usage → aucun outil → refus générique `preuve_insuffisante` | Refus **explicite** `identifiant_usage` **avant** toute planification |
| Un planificateur LLM pouvait proposer un `EQ-…` absent de la question | Garde-fou `identifiant_invente` : l'`equipment_id` doit venir de la question ou d'un outil précédent (`diagnose_report`) |

Aucun autre axe : pas de changement d'allowlist, de budget, d'outil, de corpus, de seuil `top_k`, ni d'export d'entraînement.

## Mécanisme attendu

1. Si la question contient un alias (`P-204`) **ou** (attribut fiche + nom d'équipement) **sans** `EQ-…` ni `RPT-…` → arrêt immédiat `identifiant_usage`.
2. Sinon, si un plan propose `get_equipment` / `list_events` / `get_maintenance_history` avec un `equipment_id` non ancré → arrêt `identifiant_invente`.
3. Les questions documentaires génériques (« procédure… pompe hors seuil ») restent hors de ce filtre.

## Segments pouvant régresser

| Segment | Risque | Contrôle |
|---|---|---|
| SCN-001 … SCN-005 (nominaux) | faux refus si le filtre est trop large | réussis sur gel (réussite 1,0 ; `incorrect_refusals` = 0) |
| SCN-011 (procédure + « pompe ») | confusion avec nom d'usage | test dédié : `search_knowledge` toujours appelé |
| SCN-006 / SCN-024 (équipement issu du rapport) | bloquer l'ID fourni par `diagnose_report` | `state.equipment_id` mis à jour après diagnostic |

## Ce qui ne change pas

- liste blanche (5 outils lecture seule) ;
- `allow_dynamic_tools: false` ;
- absence d'effet externe ;
- jeu gelé `scenarios_gel.jsonl` (empreinte `29fa0c7b…cd04e7`) ;
- séparation calibration / test scellé M5 ;
- `training_data_exported: false`.

## Preuves

- Config : `results/candidat/config.json`, `results/candidat/policy.yaml`
- Éval : `results/candidat/eval_scenarios_gel.json`
- Code : `agent/runner.py` (`_asks_usage_name_without_inventory_id`, `_invented_equipment_id`)
- Tests : `tests/test_candidat_ambiguite.py`
