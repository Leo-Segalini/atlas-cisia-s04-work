# Qualification des nouvelles données — online M6

**Date :** 2026-09-21  
**Principe :** pas de recréation synthétique locale ; chemins `data_pack/` uniquement.

## Rapports `reports.jsonl`

| Mesure | 2026-S1 | 2027-S1 |
|---|---:|---:|
| Volume | 40 | 60 |
| Schéma | `report_id`, `equipment_id`, `event_id`, `timestamp`, `technician_note`, `source_channel`, `period` | **identique** |
| Équipements distincts | 30 | 48 |
| `event_id` manquant | 0 | 54 |
| Note min / moy. (car.) | 145 / 176,6 | 34 / 90,7 |

### Distribution canaux 2027-S1

| Canal | n |
|---|---:|
| mobile_app | 20 |
| sms_gateway | 18 |
| web_form | 12 |
| radio_transcript | 10 |

### Qualité / biais / couverture

- **Qualité :** schéma stable → pas de migration de contrat ; notes plus courtes et SMS → risque d'ambiguïté (noms d'usage, IDs incomplets).
- **Couverture :** plus d'équipements distincts ; moins de liens `event_id`.
- **Biais canal :** sur-représentation relative du SMS vs 2026.
- **Provenance :** data pack formateur (synthétique pédagogique), **pas** données terrain réelles, **pas** augmentation locale.

## Feedback humain

Source : `data_pack/2027-S1/feedback/feedback.csv` — détail dans `docs/qualification_feedback.md`.

| Lot | n | actionnable | risque | `training_data_exported` |
|---|---:|---:|---:|---|
| b1 | 80 | 39 | 7 | false |
| b2 | 44 | 28 | 4 | false |
| all | 124 | 64 | 11 | false |

Les retours `risque` (PII, instructions) et `non_actionnable` sont **exclus** de tout entraînement. Aucun feedback n'est assimilé automatiquement à un label.

## Lien avec la cible DiagOps

Les rapports 2027 alimentent `diagnose_report` et les scénarios gelés ; le feedback alimente **une** hypothèse (ambiguïté), pas un fine-tune.
