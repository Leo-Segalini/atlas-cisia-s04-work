# ADR-0001 — Index documentaire : JSON actif, SQLite candidat local

- **Statut :** accepté pour labo / non promu en actif
- **Date :** 2026-10-06
- **Auteur :** apprenant DiagOps S04 (`work/M7`)
- **Reviewer :** auto-revue technique ; signature formateur pending

## Constat et preuve

Migration JSON→SQLite : `ranking_equal=true`, `hit_at_3=1.0`, corruption détectée, rollback JSON OK (`results/decouverte-r1/report.json`).  
Brief 2 : révocation ACL + rejet révision supersédée (`results/migration-brief2-r1/report.json`, status `passed`).

## Contraintes

Pas de téléchargement modèle ; pas de réseau requis ; ACL avant scoring ; `test_split_used=false`.

## Options

| Option | Avantages | Inconvénients |
|---|---|---|
| A — Maintenir JSON seul | simple, déjà actif | moins adapté volumes ↑ |
| B — SQLite candidat + JSON rollback | réversibilité prouvée | complexité ops |
| C — Index vectoriel cloud | qualité sémantique | souveraineté, coût, verrou |

## Choix

**B** en labo. **C écartée** (transfert / dépendance). **A** reste le chemin de référence actif.

## Impacts

- Données : mêmes documents, checksums, rôles
- Coût : local ~0 €
- Sécurité : fail-closed sur corruption / ACL incohérente
- Souveraineté : aucun fournisseur distant pour l'index
- Exploitation : pointeur `active.json`

## Gate / rollback / révision

Rollback = réactiver JSON avec `expected_sha256`. Réviser cet ADR si un embedding ou un fournisseur distant est introduit.
