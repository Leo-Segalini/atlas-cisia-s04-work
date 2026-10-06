# Contrat de migration — gelé avant mesure (brief 2)

**Gelé le :** 2026-10-06 · Empreinte cas : voir `results/migration-brief2-r1/cases_gel.json`  
**sha256 gel :** `aad26f543ff7a11984877aaa12d2cd8ce8291e1cf829c16c135e8136d13599d2`

- **Version / hash source :** export corpus `12ea939dde7016dccb6cc3a9f718394f80d531542c47db9101fc4448d3ad2da9` ; agent M6 personnel `m6-candidat-ambiguite-r1` (hors composant migré).
- **Composant / risque :** index documentaire JSON→SQLite ; risque `fuite_inter_perimetre_apres_migration`.
- **Sous-ensemble :** 7 documents actifs 2026-S1 ; cas **MIG-REV-01**, **MIG-ACL-01**, **MIG-RB-01** (distincts du seul smoke corruption).
- **Format d'export :** JSON schema_version=1 ; document_id, revision, status, allowed_roles, text, checksum_sha256, licences via manifest ; pertes tolérées : aucune sur ACL/révision.
- **Seuil qualité :** ranking calibration identique ; hit@3 inchangé ; `test_split_used=false`.
- **RTO/RPO labo :** RTO < 1 min ; RPO = dernier export checksumé ; budget temps < 5 min ; espace < 1 Mo.
- **Gates :** aucune fuite / permission élargie / action réelle.
- **Plan :** `run_personal.py` → mesure → rollback JSON.
- **Reviewer :** protocole dans `independent_review.md` ; signature formateur pending.
