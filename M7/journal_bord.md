# Journal de bord M7

| Date/durée | Brief | Hypothèse | Action | Preuve/commande | Résultat | Décision/prochaine étape |
|---|---|---|---|---|---|---|
| 2026-10-06 | clôture M6 | DoD M6 complète | journal M6 + init M7 | `work/M6/journal_bord.md` ; `init_module.py M7` | OK | démarrer cartographie |
| 2026-10-06 | B1 | smoke portabilité | unittest + lab | `python lab.py --output results/decouverte-r1` | passed hit@3=1.0 | analyser limites |
| 2026-10-06 | B1 | cartographier M6 perso + ref | docs architecture/security/resilience/portability | `architecture/*.md`, `security/*` | livré | ADR + cible |
| 2026-10-06 | B1 | outil simulé | contrat + flow | `simulated_action/` | executable=false | veille |
| 2026-10-06 | online | évaluation tabulaire | dossier | `online/dossier.md` | livré | — |
| 2026-10-06 | B2 | migration ACL/révision | gel puis mesure | `run_personal.py` → `migration-brief2-r1` | passed | revue |
| 2026-10-06 | B2 | revue / défense | IR + remédiation | `independent_review.md` | différer activation | handoff M8 |
| 2026-10-06 | veille | AI Act / supervision | entrée journal | `veille_diagops/journal.md` | contrôles dans ADR | M8 |

Budget : 14 h présentiel (dont veille), 6 h online, 20 h approfondissement — ici condensé en session agent avec preuves rejouables. Distinguer : lab/migration = **exécution réelle** ; fournisseur distant = **table** ; revue formateur = **pending signature**.
