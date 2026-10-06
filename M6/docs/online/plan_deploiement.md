# Plan de déploiement — online M6

**Date :** 2026-09-21

## Environnements

| Environnement | Rôle | Contenu autorisé |
|---|---|---|
| **Labo / préprod** | mesure, campagne, candidat | `work/M6/`, data pack local, Compose M5 référence |
| **« Prod » pédagogique** | activation contrôlée d'une version | uniquement après **décision humaine** écrite |

Il n'existe pas de prod industrielle dans ce module.

## Chaîne d'activation

1. Gates M5 + gel agent verts.
2. Campagne adversariale sans invariant ouvert.
3. Décision signée (`promouvoir` | `rejeter` | `prolonger`) dans `docs/decision_promotion.md`.
4. Si promouvoir : bascule atomique de la politique/candidat labo ; chronométrer.
5. Rollback : `m5_for_m6/operations/restauration.md` + retour `m6-baseline-r1` si besoin agent.

## État actuel

| Étape | Statut |
|---|---|
| Préprod labo candidat | actif pour mesure |
| Campagne + remédiation ADV-003 | close (réussite 1,0) |
| Décision promotion | **`prolonger`** — pas d'activation « prod » pédagogique automatique |
| Rollback documenté | oui |

## Interdits

- promotion automatique sur feedback ;
- export d'entraînement depuis `feedback.csv` brut ;
- assouplissement d'allowlist pour « faire passer » un cas.
