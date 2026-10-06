# Handoff M7 → M8

**Date :** 2026-10-06  
**Depuis :** `work/M7`  
**Vers :** module M8 (nouveau projet — référence commune non créée ici)

## Livré

- Architecture courante / cible + ADR-0001 (index) + ADR-0002 (outil simulé)
- Threat model, red team RT-01…09, risques résiduels
- Portabilité lab + migration brief2 (révocation, révision, rollback)
- Online dossier (cas tabulaire autonome)
- Veille M7 datée
- Décision : **différer** activation effets / bascule index

## Questions ouvertes

| # | Question | Responsable | Échéance |
|---|---|---|---|
| 1 | Qui signe la revue indépendante et la promotion d'architecture ? | Formateur S04 + lead technique | Avant toute bascule hors labo |
| 2 | RTO/RPO métier hors machine apprenant ? | Exploitation pédagogique | Avant « prod » élargie |
| 3 | Un outil à effet réel (ticket, CMMS) est-il autorisé, avec quel bac à sable juridique ? | Conformité + métier | **Avant** tout `executable: true` |
| 4 | LLM cloud sur le planificateur : DPA / localisation ? | Architecture + conformité | Avant branchement chemin critique |

## Preuves à joindre pour M8

`architecture/`, `security/`, `results/decouverte-r1/report.json`, `results/migration-brief2-r1/report.json`, `veille_diagops/journal.md`, `migration_exercise/*`.
