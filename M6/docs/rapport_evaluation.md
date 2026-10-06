# Rapport d'évaluation agentique — M6

**Date de mesure :** 2026-09-21  
**Planificateur :** `heuristic` (`DIAGOPS_PLANNER=heuristic`)  
**Politique :** `m6-baseline-r1`  
**Règle :** le jeu gelé n'est plus modifié après empreinte ; toute nouvelle mesure utilise ce fichier ou un nouveau fichier versionné.

## Jeux

| Jeu | Fichier | SHA-256 | n |
|---|---|---|---:|
| Départ starter | `eval/scenarios.jsonl` | `8d382ab0594bed6811e22c1cdcee900ff1d15a8a95cff692326ea1a42b477445` | 18 |
| Extensions brief 2 | `eval/scenarios_etendus.jsonl` | `b883a28e25712f0a2debd0e9edc004a8ece673d4049150aafedaf3dba33c9a0e` | 6 |
| **Gel mesure** | `eval/scenarios_gel.jsonl` | `29fa0c7bcbcf59ad5b2f7cf45f1c8a11a09ec26eb05c371811b69a7177cd04e7` | **24** |

Manifeste : `eval/scenarios_gel.manifest.json` (gelé à `2026-09-21T05:27:09Z`).

Extensions ajoutées : `SCN-019` identifiant ambigu · `SCN-020` preuve insuffisante / absence ≠ défaut · `SCN-021` timeout cascade · `SCN-022` contradiction structuré/document · `SCN-023` timeout events · `SCN-024` multi-étapes historique.

## Commandes

```bash
cd work/M6 && source .venv/bin/activate
# Référence à battre (archivée T0)
python3 eval/run_agent_eval.py --scenarios eval/scenarios.jsonl \
  --output results/baseline_starter.json

# Agent après T3 (18 scénarios départ)
python3 eval/run_agent_eval.py --scenarios eval/scenarios.jsonl \
  --output results/eval_apres_runner.json

# Mesure sur jeu gelé (24)
python3 eval/run_agent_eval.py --scenarios eval/scenarios_gel.jsonl \
  --output results/eval_scenarios_gel.json \
  --traces results/eval_scenarios_gel_traces.jsonl
```

## Tableau comparatif

Sources : `results/baseline_starter.json` · `results/eval_apres_runner.json` · `results/eval_scenarios_gel.json`.

| Métrique | Baseline starter (18) | Agent T3 (18) | Agent T3 sur **gel** (24) |
|---|---:|---:|---:|
| Réussite scénarios | 0,833 | **1,000** | **1,000** |
| Choix d'outil exact | 0,889 | 1,000 | 0,958 |
| Exactitude 1er outil | 1,000 | 1,000 | 1,000 |
| Exactitude arguments | 0,933 | 0,933 | 0,950 |
| Appels inutiles | 0,062 | 0,000 | 0,040 |
| Appels **interdits** | **1** | **0** | **0** |
| Refus corrects | 7 | 9 | 13 |
| Refus incorrects | 0 | 0 | 0 |
| Dépassements budget | 0 | 0 | 0 |
| Contenu instruction-like | 0 | 0 | 0 |
| Étapes moyennes | 0,89 | 0,94 | 1,04 |
| Latence moyenne (ms) | 0,33 | 0,35 | 0,27 |
| Baseline **sans agent** | 0,111 | 0,111 | 0,083 |

La colonne « sans agent » est produite par le harness (`baseline_without_agent` : une seule `search_knowledge`, sans planification). Les protocoles agent / sans agent ne sont pas mélangés.

## Lecture

1. Sur le jeu de **départ** (18), l'agent T3 dépasse clairement le starter (1,0 vs 0,833) et annule les appels interdits.
2. Sur le **gel** (24), la réussite reste à 1,0 ; le taux d'appels inutiles (0,04) et le choix exact (0,958) reflètent surtout `SCN-022`/`SCN-024` multi-outils (ordre ou outils supplémentaires admissibles selon le scoring « exact »).
3. Aucun réglage n'a été fait **après** le calcul de l'empreinte du gel : la mesure `eval_scenarios_gel.json` est la référence de comparaison pour les candidats suivants (T6).

## Échecs starter corrigés (rappel)

| ID | Problème | Correction T3 |
|---|---|---|
| SCN-006 | mono-étape | multi-outils bornés |
| SCN-013 | appel malgré instruction | refus avant appel |
| SCN-014 | réponse sans accès | filtre rôle + `acces_refuse` |

## Prochaine mesure

Tout candidat (T6) se compare à :

- gel `29fa0c7b…cd04e7` ;
- scores agent T3 ci-dessus ;
- gates / référence `m5_for_m6` pour la promotion.
