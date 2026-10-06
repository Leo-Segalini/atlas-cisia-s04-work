# Politique des données et des accès — M7

**Date :** 2026-10-06  
Le rôle passé au banc est un **argument de démonstration**, pas une authentification de production.

| Actif | Propriétaire / finalité | Sensibilité | Rôles autorisés | Localisation / transfert | Rétention / suppression | Sauvegarde / RPO | Preuve |
|---|---|---|---|---|---|---|---|
| Corpus + index | Formateur / assistance procédure | Interne pédagogique | public, technicien, superviseur, auditeur (ACL/doc) | `data_pack/` local ; pas de transfert cloud index | durée module ; pas de copie hors labo | copie FS ; RPO labo = dernier export checksumé | `lab.py`, MIG-ACL-01 |
| Données outils (EQ, EVT, RPT) | Formateur / diagnostic lecture | Interne | selon outil + rôle agent | CSV/JSONL data_pack | module | data_pack amont | contrats M6 |
| Questions + traces agent | Apprenant / mesure | Interne ; pas de PII volontaire | opérateur labo | `work/M6/results/` | 30 j déclaré M6 | local | politique trace M6 |
| Feedback | Formateur / amélioration | **Risque PII** dans commentaires | qualify script | `2027-S1/feedback/` | exclusion `risque` ; pas d'entraînement auto | — | `qualification_feedback.md` |
| Secrets / tokens HF | Apprenant | Secret | aucun en dépôt | `.env` local gitignoré | révocation compte | — | `.env.example` M6 |

## Règles

1. Droits **avant** classement et avant toute génération.
2. Document `superseded` → refus import (MIG-REV-01).
3. Révocation de rôle → reconstruction index ; pas d'élargissement silencieux.
4. Feedback `risque` → jamais prompt ni dataset.
5. Chiffrement disque / isolation OS : **à concevoir hors POC** (limite assumée).
