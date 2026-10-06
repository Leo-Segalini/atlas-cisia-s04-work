# Évaluation d'une architecture IA — brief online autonome

**Date :** 2026-10-06  
**Cas :** classificateur / assistant de **tri de criticité d'équipement** (tabulaire local, sklearn-like) — **sans** RAG ni agent requis.  
Inspiration continue DiagOps : fiches `equipment.csv` + règles métier synthétiques.

## Cas et procédure

| Élément | Contenu |
|---|---|
| Utilisateur | technicien maintenance (labo) |
| Finalité | prioriser les équipements à inspecter |
| Procédure | 1) cadrer 2) inventorier données 3) mesurer qualité/coût/droits 4) comparer alternative 5) décider |
| Sources | data_pack equipment (synthétique) ; pas de données personnelles |

## Données et cycle de vie

| Étape | Responsable | Destinataire | Droits | Rétention |
|---|---|---|---|---|
| Source CSV | formateur | apprenant | lecture labo | durée module |
| Préparation | apprenant | pipeline local | local | artefacts `work/` |
| Entraînement | apprenant | modèle local | local | versionné hash |
| Exploitation | démo locale | technicien fictif | rôle démo | session |
| Surveillance | apprenant | journal métriques | local | 30 j |
| Correction / suppression | apprenant | — | effacer artefacts | fin module |

## Grille

| Axe | Constat | Mesure ou estimation | Source / protocole | Alternative | Risque / condition |
|---|---|---|---|---|---|
| qualité / capacité / latence | modèle tabulaire suffisant en labo | estimation : <100 ms / pred locale | split train/val local ; **pas** test scellé pour régler | règles métier seules | sur-apprentissage si fuite |
| disponibilité / stockage / packaging | FS local | mesure : Mo-order CSV | inventaire fichiers | SQLite features | panne machine unique |
| coût / empreinte / compétences | ≈ 0 € cloud | estimation | pas d'API | service ML cloud | transfert + verrou |
| biais / confidentialité / supervision | biais site/équipement possibles ; pas de PII | revue manuelle distributions | comptages colonnes | revue humaine des priorités | supervision obligatoire |

## Proposition et restitution

- **Cible :** modèle local versionné + revue humaine des priorités hautes.
- **Évolution priorisée :** (1) documentation des features (2) monitoring drift simple (3) pas de cloud.
- **Acteurs à consulter :** formateur, référent sécu pédagogique, (juridique si hors POC).
- **Succès :** reproductibilité locale + absence de données perso + décision humaine sur les cas limites.

Support one-pager = ce dossier ; journal : `journal_bord.md`.
