# Journal d'exécution — migration brief 2

**Date :** 2026-10-06

## Commandes

```bash
cd work/M7
python migration_exercise/run_personal.py --output results/migration-brief2-r1
```

## Chronologie

| Étape | Résultat |
|---|---|
| Gel `cases_gel.json` | sha256 `aad26f54…599d2` **avant** mutations |
| Export corpus | sha256 `12ea939d…2da9` |
| MIG-REV-01 | **passed** — superseded refusé |
| MIG-ACL-01 | **passed** — `DOC-CHILL-TEMP-001` : `technicien` retiré ; hits technicien `[]` (DOC-DATA-ACCESS-001 n'avait pas ce couple de rôles pour le fallback initial) |
| MIG-RB-01 | **passed** — ranking_equal, rollback_equal, corruption_detected ; migration_ms ≈ 0,95 |
| status global | **passed** |

## Erreurs rencontrées

Aucune bloquante. Note : la révocation a porté sur `DOC-CHILL-TEMP-001` (premier document technicien+superviseur), pas sur `DOC-DATA-ACCESS-001` (souvent réservé superviseur) — comportement conforme au script de fallback documenté.
