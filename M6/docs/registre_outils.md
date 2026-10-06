# Registre des outils — M6

**Date de gel documentaire :** 2026-09-21  
**Politique liée :** `agent/policy.yaml` (`m6-baseline-r1`)  
**Règle :** un outil absent de ce registre n'existe pas pour l'agent. Une fiche incomplète interdit la mise en service.

Les cinq adaptateurs sont décrits à partir de leur contrat `SPEC` dans `tools/*.py`,
vérifiés par observation le 2026-09-21. Aucun sixième outil n'est autorisé.

## Outils distribués

| Outil | Finalité | Arguments | Résultat | Source de vérité | Rôles | Timeout | Limite |
|---|---|---|---|---|---|---|---|
| `search_knowledge` | fonder une réponse sur une procédure ou une politique | `query`, `top_k` | `document_id`, `title`, `revision`, `excerpt`, `score` | corpus actif du manifeste | technicien, superviseur, auditeur, public | 1500 ms | 3 |
| `get_equipment` | lire la fiche d'inventaire | `equipment_id` | type, site, criticité, mise en service, fabricant, puissance | `equipment.csv` | technicien, superviseur, auditeur | 800 ms | 1 |
| `list_events` | lister les événements récents | `equipment_id`, `severity`, `limit` | événements triés du plus récent au plus ancien | `events.csv` | technicien, superviseur, auditeur | 1000 ms | 10 |
| `get_maintenance_history` | lire les dernières interventions | `equipment_id`, `limit` | interventions, issue, durée d'arrêt | `maintenance_history.csv` | technicien, superviseur, auditeur | 1200 ms | 10 |
| `diagnose_report` | lire un rapport et en extraire le squelette DiagOps | `report_id` | équipement, symptôme, indice de sévérité, preuves, revue humaine | `reports.jsonl` | technicien, superviseur, auditeur | 1000 ms | 1 |

## Fiche par outil

### `search_knowledge`

- **finalité :** retrouver les passages de procédure ou de politique qui fondent une réponse citée.
- **arguments et contraintes :**
  - `query` (string, obligatoire, 3–200 caractères) ;
  - `top_k` (entier, optionnel, 1–3, défaut 3).
- **résultat et champs exposés :** `document_id`, `title`, `revision`, `excerpt` (fenêtre ~240 car.), `score` lexical.
- **source de vérité et fraîcheur :** `data_pack/2026-S1/knowledge/` — documents `status=active` du manifeste, checksum SHA-256 vérifié à la lecture. Les révisions remplacées (ex. DOC-LOTO-001) ne sont pas servies.
- **autorisation :** rôles `technicien`, `superviseur`, `auditeur`, `public`. Filtrage supplémentaire par `allowed_roles` du document **avant** scoring. Un rôle hors liste blanche d'outil est refusé par le registre ; un rôle admis mais absent de `allowed_roles` du document ne voit pas l'extrait.
- **timeout et limite de résultats :** 1500 ms ; max 3 documents. Un `top_k` > 3 est refusé à la validation. Dépassement de durée → erreur d'outil / arrêt politique.
- **données sensibles :**
  - **lu :** texte intégral des documents actifs admissibles pour le rôle ;
  - **rendu :** excerpt court + métadonnées ;
  - **tracé :** `argument_keys`, empreinte, `row_count`, `source` — jamais le texte ni la query en clair.
- **erreurs connues :**

| Cas | Signal | Effet |
|---|---|---|
| aucun document pour rôle + requête | `reason` explicite, `rows` vides | agent doit refuser / preuve insuffisante |
| checksum invalide | `ToolError` | arrêt (`stop_on_tool_error`) |
| corpus indisponible | `ToolUnavailable` | mode dégradé |

- **mode dégradé :** résultat vide + motif ; la réponse doit refuser plutôt que d'inventer. Observé 2026-09-21 : query `zzzzinexistant` en rôle `public` → motif « aucun document actif admissible… ».
- **preuve :** `SCN-001` (nominal), `SCN-016` ; filtres d'accès : `SCN-014` (échec baseline — à corriger en T3).

### `get_equipment`

- **finalité :** lire la fiche d'inventaire d'un équipement identifié.
- **arguments et contraintes :** `equipment_id` (string, obligatoire, motif `^EQ-[A-Z]+-\d+$`). Jamais un nom d'usage.
- **résultat et champs exposés :** `equipment_id`, `equipment_type`, `site_id`, `criticality`, `commissioning_date`, `manufacturer`, `rated_power_kw`.
- **source de vérité et fraîcheur :** `data_pack/2026-S1/equipment/equipment.csv` (table figée de session).
- **autorisation :** `technicien`, `superviseur`, `auditeur`. Le rôle `public` est exclu : inventaire interne.
- **timeout et limite de résultats :** 800 ms ; exactement 0 ou 1 ligne.
- **données sensibles :** aucune PII ; site et criticité restent internes → non exposés en trace.
- **erreurs connues :**

| Cas | Signal | Effet |
|---|---|---|
| identifiant inconnu | `reason=identifiant inconnu : …`, rows vides | pas de conjecture d'équipement |
| pattern invalide | validation registre | refus avant appel |
| table absente | `ToolUnavailable` | mode dégradé |

- **mode dégradé :** résultat vide + motif. Observé : `EQ-ZZZ-999` → `identifiant inconnu : EQ-ZZZ-999`.
- **preuve :** `SCN-002`, `SCN-007` ; refus ID inconnu : `SCN-008`.

### `list_events`

- **finalité :** lister les événements récents rattachés à un équipement.
- **arguments et contraintes :**
  - `equipment_id` (obligatoire, même motif EQ-…) ;
  - `severity` optionnel ∈ {`low`,`medium`,`high`,`critical`} ;
  - `limit` optionnel 1–10 (défaut 5).
- **résultat et champs exposés :** `event_id`, `equipment_id`, `start_at`, `end_at`, `event_type`, `severity` — tri du plus récent au plus ancien.
- **source de vérité et fraîcheur :** `data_pack/2026-S1/events/events.csv`.
- **autorisation :** `technicien`, `superviseur`, `auditeur`.
- **timeout et limite de résultats :** 1000 ms ; max 10. `truncated=true` si plus d'événements existent.
- **données sensibles :** aucune PII.
- **erreurs connues :** sévérité hors énumération (validation) ; table indisponible ; liste vide ≠ preuve d'absence de défaut.
- **mode dégradé :** rows vides + motif `aucun événement pour …`. Observé : `EQ-FAN-304` retourne des lignes (4) sans troncature pour limit=5.
- **preuve :** `SCN-003` ; résultat vide attendu : `SCN-010`.

### `get_maintenance_history`

- **finalité :** lire les dernières interventions enregistrées pour un équipement.
- **arguments et contraintes :** `equipment_id` obligatoire ; `limit` 1–10 (défaut 5).
- **résultat et champs exposés :** `maintenance_id`, `event_id`, `opened_at`, `closed_at`, `intervention_type`, `outcome`, `downtime_minutes`.
- **source de vérité et fraîcheur :** `data_pack/2026-S1/maintenance/maintenance_history.csv`.
- **autorisation :** `technicien`, `superviseur`, `auditeur`.
- **timeout et limite de résultats :** 1200 ms ; max 10. Fenêtre courte → `truncated` possible.
- **données sensibles :** notes internes éventuelles non exposées (champs listés seulement) ; aucune PII attendue.
- **erreurs connues :** identifiant sans historique → rows vides + motif ; table absente → `ToolUnavailable`.
- **mode dégradé :** **une récidive ne se déduit pas d'un historique tronqué**. Observé : `EQ-CONV-003` avec `limit=3` → `truncated=true` (plus de 3 interventions).
- **preuve :** `SCN-004` ; lien feedback b1 (historique insuffisant pour juger une récidive).

### `diagnose_report`

- **finalité :** lire un rapport technicien et en extraire le squelette du contrat DiagOps (lecture structurée, **pas** un diagnostic validé).
- **arguments et contraintes :** `report_id` obligatoire, motif `^RPT-\d{4}S\d-\d{4}$`.
- **résultat et champs exposés :** `report_id`, `equipment_id`, `symptom` (extrait lexical), `severity_hint` (via `events.csv` si `event_id`), `evidence`, `requires_human_review` **toujours true**.
- **source de vérité et fraîcheur :** `data_pack/2026-S1` et `2027-S1` `reports/reports.jsonl` ; sévérité liée dans `events.csv`.
- **autorisation :** `technicien`, `superviseur`, `auditeur`.
- **timeout et limite de résultats :** 1000 ms ; 0 ou 1 ligne. Aucun modèle génératif appelé.
- **données sensibles :** le texte libre du rapport peut citer une personne — **seul** le symptôme extrait est rendu ; le texte brut n'est pas tracé.
- **erreurs connues :** rapport inconnu → rows vides + motif. Observé : `RPT-2099S1-9999` → `rapport inconnu : RPT-2099S1-9999`.
- **mode dégradé :** aucune hypothèse sans rapport ; `requires_human_review` reste vrai même en succès.
- **preuve :** `SCN-005`, `SCN-018` ; multi-preuves attendues : `SCN-006` (échec baseline — runner mono-étape).

## Interdits

- aucun outil n'envoie, n'écrit, ne commande, ne modifie ni ne déclenche ;
- aucune connexion arbitraire n'est exposée au modèle ;
- aucun outil n'est ajouté sans scénario de test associé ;
- aucun argument brut n'apparaît dans les traces ;
- un résultat d'outil est une **donnée**, jamais une instruction système.

## Journal des modifications

| Date | Outil | Modification | Motif | Décidée par |
|---|---|---|---|---|
| 2026-09-21 | les cinq | fiches complétées + modes dégradés observés | T1 spec travail | apprenant M6 |
| | | | | |
