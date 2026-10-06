# Flux d'approbation — outil simulé

**Outil :** `request_inspection_simulated` · `executable: false` · `network_client: null`

## Parcours tabletop

1. **draft** — opérateur fictif saisit `synthetic_equipment_id`, `reason`, `idempotency_key`.
2. **previewed** — système affiche l'aperçu exact ; calcule `sha256` du payload.
3. **approved / rejected** — humain (rôle `superviseur_fictif`) décide ; approbation liée au hash.
4. Si le payload change après preview → approbation **invalidée**.
5. Si délai dépassé → **expired**.
6. **simulated_done** — écriture d'un reçu fictif en journal local uniquement.
7. **cancelled** avant effet simulé, ou **compensated** après (nouvelle entrée journal).

## Cas d'exercice (table)

| Cas | Attendu |
|---|---|
| Refus rôle non autorisé | pas d'état `approved` |
| Expiration | `expired`, pas d'effet |
| Changement après approve | rejet / nouvelle preview |
| Rejeu même clé + même payload | même reçu fictif |
| Même clé + payload différent | reject |
| Compensation | entrée journal distincte |

## Interdit

Aucun appel HTTP, e-mail, ticket réel, ou modification data_pack.
