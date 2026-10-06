# Objectifs de reprise — M7

**Date :** 2026-10-06 · Périmètre labo pédagogique (pas de SLA industriel).

| Objectif | Valeur labo | Preuve |
|---|---|---|
| RTO index actif | < 1 min (réactivation JSON) | `recovery_ms` ≈ 4 ms sur discovery |
| RPO corpus | dernier export `source_export_sha256` | report lab / brief2 |
| RTO agent | redémarrage process local | — |
| Mode dégradé | refus motivé, pas d'invention | SCN timeout / unavailable |

## Procédure rollback index

1. Conserver `corpus.json` et son sha256.
2. Sur panne SQLite : ne pas réparer en place aveuglément.
3. `activate(..., "corpus.json", "json", expected_sha256=...)`.
4. Rejouer calibration (split calibration only).

## Condition hors labo

Nommer RTO/RPO métier + responsable avant toute « prod » pédagogique élargie (question ouverte M8).
