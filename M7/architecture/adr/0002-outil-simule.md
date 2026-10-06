# ADR-0002 — Outil à effet simulé `request_inspection_simulated`

- **Statut :** accepté en tabletop only (`executable: false`)
- **Date :** 2026-10-06
- **Auteur :** apprenant DiagOps S04

## Constat

M6 interdit les effets externes. M7 doit spécifier un outil à effet **sans** l'exécuter sur un système réel.

## Options

| Option | Décision |
|---|---|
| Brancher un ticket réel | **écartée** — effet réel |
| Spécifier contrat + exercice table | **retenue** |
| Ignorer l'outil à effet | écartée — brief 1 §7 |

## Choix

Contrat `simulated_action/contract.json` : aperçu hashé, approbation humaine, expiration, idempotency, compensation journalisée, `network_client: null`.

## Gate

Interdit d'entrer dans le chemin de référence agent tant qu'une décision M8+ et une veille mise à jour ne l'autorisent. Voir `approval_flow.md`.
