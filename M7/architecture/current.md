# Architecture observée — DiagOps M6 → M7

**Date :** 2026-10-06  
**Référence commune :** `diagops-m6-reference-r1` (`data_pack/2026-S1/reference_runs/m6_for_m7/`) — starter M6 avec échecs connus SCN-006/013/014, ADV-001/006.  
**État personnel figé :** `work/M6/` — politique `m6-candidat-ambiguite-r1` (sha256 policy `1e7be504…`), gel scénarios `29fa0c7b…cd04e7`, décision promotion **`prolonger`**.

Les deux états ne sont **pas** mélangés dans une comparaison : la référence commune sert d'audit des limites starter ; les mesures ci-dessous citent l'état personnel quand une preuve locale existe.

## Cartographie

```text
[Technicien] --question--> [BoundedAgent / policy.yaml]
                              | allowlist + budget
                              v
                    [Heuristic|Ollama|HF Planner] --suggestion--> [Registry]
                              ^                                        |
                              | données ≠ instruction                  v
                    [Tool adapters RO] <---- data_pack (knowledge, EQ, EVT, RPT)
                              |
                              v
                    [Trace JSONL] --> [Eval harness] --> [results/]
[Feedback CSV] --> [qualify_feedback.py] --> classes ; jamais labels auto
[M5 Compose/ref] <-- rollback --> diagops-m5-reference-r1
```

| Composant | Source/version/hash | Propriétaire | Données | Dépendance | Preuve d'exécution |
|---|---|---|---|---|---|
| Agent borné | `work/M6/agent/runner.py` + `policy.yaml` `m6-candidat-ambiguite-r1` | apprenant M6 | questions, traces | PyYAML, outils RO | `pytest` ; gel réussite 1,0 |
| Registre outils | `work/M6/agent/registry.py` | apprenant M6 | contrats args | data_pack | `tests/test_tool_contracts.py` |
| Index / corpus | `data_pack/2026-S1/knowledge/` | formateur | docs + ACL | FS local | `lab.py` hit@3=1,0 |
| Planificateur | heuristic (défaut) ; ollama/hf optionnels | apprenant | prompt plan | réseau si HF/Ollama | `docs/modeles_planificateur.md` |
| Feedback | `2027-S1/feedback/feedback.csv` | formateur | commentaires | CSV | `qualification_feedback.md` |
| Gates M5 | `m5_for_m6/gates/gates.json` | référence | métriques RAG | — | rappel non recalibré |

## Frontières de confiance

| Frontière | Contenu non fiable | Contrôle |
|---|---|---|
| Question utilisateur | injection, hors périmètre | refus `instruction_dans_question`, hors scope |
| Sortie outil | instruction emballée | `treat_tool_output_as_data`, INV-08 |
| Document corpus | empoisonnement / révision | statut active, ACL avant score |
| Feedback | PII, consigne système | classe `risque`, pas d'entraînement |
| Fournisseur LLM | suggestion d'outil inventée | allowlist + `identifiant_invente` |

## Écarts

| Observé (personnel M6) | Référence `m6_for_m7` | Cible M7 |
|---|---|---|
| Multi-étapes + refus usage ID | Starter 1 étape ; échecs SCN-006/013/014 | Conserver bornes ; pas d'outil à effet sans ADR |
| Campagne ADV 1,0 après remédiation | ADV-001/006 en échec sur référence | Traiter risques starter comme dette si on repart de la référence |
| Décision `prolonger` | Aucune promotion | Promotion humaine obligatoire |
