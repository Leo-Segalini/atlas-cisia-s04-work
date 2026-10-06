# Scénarios de résilience — M7

**Date :** 2026-10-06  
Légende type : `exécuté` (copie locale) · `table` (simulation documentée).

| # | Scénario | Type | Impact | Détection | Réponse | Reprise | Preuve |
|---|---|---|---|---|---|---|---|
| 1 | Index / modèle indisponible | exécuté | pas de retrieval | ValueError index absent | refus | restaurer JSON | tests missing index ; lab |
| 2 | Fournisseur distant inaccessible | table | plan LLM down | timeout/erreur HTTP | fallback heuristique M6 | N/A local | `providers.py` fallback ; **non testé live** |
| 3 | Corpus partiellement obsolète | exécuté | mauvaise révision | status ≠ active | refus import | garder export sain | MIG-REV-01 |
| 4 | Montée en charge / budget épuisé | exécuté (agent) | arrêt | budget_* | refus | — | ADV-004 ; policy bounds |
| 5 | Outil lent / incohérent | exécuté | timeout | erreur_outil | arrêt | — | ADV-005 ; SCN-023 |
| 6 | Compromission document | exécuté | instruction dans texte | contenu = donnée | pas d'élargissement | — | RT-02 |
| 7 | Demande sans droit | exécuté | pas de doc | ACL avant score | résultat filtré / refus | — | RT-05 ; SCN-014 |
| 8 | Perte / corruption index | exécuté | panne candidat | lecture échoue | rollback pointeur | JSON hash | lab ; MIG-RB-01 |

## Non testé explicitement

- charge concurrente multi-utilisateurs ;
- panne réseau réelle Ollama/HF ;
- restauration hors machine labo.
