# Architecture cible — DiagOps M7

**Statut :** **non approuvée** — proposition à défendre ; smoke test ≠ approbation.  
**Date :** 2026-10-06  
**Décision proposée :** **différer** l'activation d'un outil à effet ; **maintenir** lecture seule + index JSON actif ; **autoriser** SQLite en candidat d'index seulement après revue.

## Besoin et contraintes

| Contrainte | Valeur |
|---|---|
| Public | techniciens / superviseurs pédagogiques |
| Capacité | RAG lexical + agent RO borné |
| Localisation | labo local ; cloud LLM optionnel non promu |
| Droits | ACL documentaires avant scoring |
| Coût | zéro service payant requis |
| Disponibilité | mode dégradé refus motivé |
| Compétences | Python 3.11+, pytest, YAML |

## Diagramme cible (différences)

```text
[Identité rôle] → [ACL filter] → [Index actif JSON*|SQLite candidat]
                                      ↓
                              [Bounded agent RO]
                                      ↓
                         [Outil à effet SIMULÉ hors chemin ref]
                                      ↓
                         [Approbation humaine + idempotency]
```

\* Index actif de référence reste JSON jusqu'à décision.

| Différence vs actuel | Constat | Preuve | ADR |
|---|---|---|---|
| Index SQLite candidat | parité lexicale, rollback OK | `results/decouverte-r1`, `migration-brief2-r1` | ADR-0001 |
| Outil inspection simulé | hors chemin référence | `simulated_action/` | ADR-0002 |
| LLM cloud non dans chemin critique | souveraineté / transfert | veille M6/M7 | ADR-0001 |

## Gates avant migration

- [x] Zéro fuite de droits (tests + MIG-ACL-01)
- [x] Métadonnées / provenance conservées (export checksum)
- [x] Écart qualité mesuré (hit@3 = 1,0 ; ranking_equal)
- [x] Retour arrière rejoué (corruption détectée)
- [x] Risques bloquants traités ou acceptés documentés
- [ ] Revue indépendante **signée formateur** (auto-revue technique faite ; signature externe pending)
- [ ] Décision humaine d'activation

## Décision finale (proposition)

**Différer** la bascule d'index actif vers SQLite et **refuser** tout outil à effet réel.  
Réouverture si : signature reviewer, RTO/RPO nommés hors labo, et réponse aux 3 questions du passage M6→M7.
