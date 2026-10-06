# Politique d'exécution — M6

**Fichier :** `agent/policy.yaml`  
**Identifiant actif labo :** `m6-candidat-ambiguite-r1` (après T6 ; baseline archivée `m6-baseline-r1`)  
**Date :** 2026-09-21

Chaque valeur ci-dessous est une décision. La modifier est un **candidat** (un axe), à comparer avant promotion.

## Liste blanche

| Outil | Motif d'autorisation |
|---|---|
| `search_knowledge` | procédures / politiques citées |
| `get_equipment` | fiche inventaire typée |
| `list_events` | événements structurés |
| `get_maintenance_history` | interventions structurées |
| `diagnose_report` | lecture de rapport (pas diagnostic validé) |

Tout outil absent est refusé (`stop_reason = outil_hors_liste`), même s'il était enregistré.  
`allow_dynamic_tools: false` — l'agent ne peut pas s'ajouter de capacité (test `test_politique_autorisant_les_outils_dynamiques_refusee`).

## Budget

| Clé | Valeur | Pourquoi | Menace couverte | Test |
|---|---:|---|---|---|
| `max_steps` | 4 | suffit pour `SCN-006` (rapport → fiche → procédure) sans boucle libre | boucle infinie | `test_budget_d_etapes_applique` |
| `max_tool_calls` | 4 | aligné sur les étapes | même | idem |
| `max_duration_ms` | 8000 | labo local ; plafond code 30000 | latence / DoS | load_policy refuse > 30000 |
| `max_repeated_calls` | 1 | un seul appel identique (empreinte) | `ADV-004` répétition coûteuse | `test_appel_repete_detecte` |
| `max_result_rows` | 10 | borne registre / politique | exfiltration volumineuse | contrats outils |

Plafonds code durs : `HARD_MAX_STEPS = 8`, `HARD_MAX_DURATION_MS = 30000`. La politique ne peut pas les dépasser.

## Exécution

| Clé | Valeur | Effet |
|---|---|---|
| `stop_on_tool_error` | true | erreur d'outil → arrêt (`erreur_outil`) |
| `require_evidence` | true | pas de réponse sans preuve |
| `treat_tool_output_as_data` | true | contenu récupéré ≠ instruction (`ADV-002`, INV-08) |
| `allow_dynamic_tools` | false | INV-02 |

## Candidat T6 — refus identifiant d'usage

Hors YAML (code `runner.py`), un seul axe ajouté :

| `stop_reason` | Déclencheur | Scénarios |
|---|---|---|
| `identifiant_usage` | alias `P-…` ou attribut+nom sans `EQ-`/`RPT-` | SCN-009, SCN-019 |
| `identifiant_invente` | `equipment_id` non ancré question/état | planificateur LLM |

Détail : `docs/hypothese_candidat.md` · décision : `docs/decision_promotion.md`.

## Traces

Enregistré : `step`, `tool`, `argument_keys`, `argument_fingerprint`, `row_count`, `source`, `elapsed_ms`, `outcome`.

Interdit : `document_text`, `raw_arguments`, `private_reasoning`, `personal_data`.

Rétention : **30 jours** (labo pédagogique). Hors labo, réévaluer en veille M6/M7 — ce n'est pas une durée industrielle figée.

## Rôle par défaut

`role: technicien`. Un scénario peut surcharger le rôle via le harness ; le filtrage documentaire s'applique **avant** lecture (`SCN-014`).

## Planificateur (modèle)

La politique d'outils reste indépendante du **planificateur** :

| Mode | Env | Usage |
|---|---|---|
| `heuristic` (défaut) | `DIAGOPS_PLANNER=heuristic` | reproductible, tests, gates |
| `ollama` | `DIAGOPS_PLANNER=ollama` | suggestion locale |
| `huggingface` | `DIAGOPS_PLANNER=huggingface` | suggestion cloud |

Le planificateur LLM **propose** un outil ; le registre et le budget **décident**. Un échec LLM retombe sur l'heuristique. Voir `docs/modeles_planificateur.md`.
