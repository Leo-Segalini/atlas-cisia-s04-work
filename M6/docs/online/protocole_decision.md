# Protocole candidat et décision — online M6

**Réutilise :** Tâche 5 (`docs/qualification_feedback.md`) · Tâche 6 (`docs/hypothese_candidat.md`, `docs/decision_promotion.md`)

## Protocole (une hypothèse)

1. Qualifier le feedback → retenir un thème actionnable (ambiguïté nom d'usage).
2. Modifier **un** axe : politique de refus (`identifiant_usage` / `identifiant_invente`).
3. Mesurer sur le jeu **gelé** (empreinte `29fa0c7b…cd04e7`) — jamais sur un test scellé M5 pour régler.
4. Comparer à `m6-baseline-r1` et aux gates `m5_for_m6`.
5. Décider humainement ; rollback documenté.

## Décision T6 (inchangée dans le principe)

| Champ | Valeur |
|---|---|
| Candidat | `m6-candidat-ambiguite-r1` |
| Différence unique | motif de refus + garde-fou anti-invention d'ID |
| Gel | réussite 1,0 ; interdits 0 |
| Décision | **`prolonger`** |
| Motif | campagne / déploiement humain non finalisés au moment T6 ; après T8 la remédiation ADV-003 est close mais la promotion reste humaine |

## Remédiation post-campagne (T8)

Échec initial ADV-003 (appel `search_knowledge` induit par injection de chemin) corrigé dans le planificateur heuristique **sans** élargir l'allowlist. Voir `adversarial/remediation.md`.
