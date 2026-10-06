# Essai de portabilité — brief 1

**Date :** 2026-10-06

## Démonstration kit

```bash
cd work/M7
python -m unittest discover -s tests -v
python lab.py --output results/decouverte-r1
```

| Mesure | Valeur |
|---|---|
| status | passed |
| documents | 7 |
| hit@3 before/after | 1.0 / 1.0 |
| ranking_equal | true |
| corruption_detected | true |
| migration_ms | ~1.8 |
| export sha256 | `12ea939dde7016dccb6cc3a9f718394f80d531542c47db9101fc4448d3ad2da9` |

Le score **lexical** est conservé : changement de stockage, pas de modèle génératif.

## Incompatibilité provoquée (au-delà du smoke)

| Essai | Action | Constat | Remédiation |
|---|---|---|---|
| Révision obsolète | `status=superseded` sur export copie | `read_export` → ValueError | conserver export sain ; MIG-REV-01 |
| ACL révoquée | retirer `technicien` puis migrer SQLite | doc absent des hits technicien | reconstruction depuis export ACL ; MIG-ACL-01 |

Commandes : `python migration_exercise/run_personal.py --output results/migration-brief2-r1`.

## Limites

Pas de mesure de qualité de réponses LLM, pas de multi-utilisateur, latences non extrapolables. Reproduire seulement `lab.py` **ne valide pas** le brief 2 — d'où les cas MIG-* gelés avant mesure.
