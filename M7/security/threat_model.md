# Modèle de menaces — M7

**Date :** 2026-10-06 · Périmètre : copies locales synthétiques + agent M6 personnel.

| Actif / frontière | Acteur et capacité | Menace | Impact C2/C7 | Contrôle | Test / preuve | Limite |
|---|---|---|---|---|---|---|
| Corpus → classement | rédacteur document | instruction indirecte | C2 fuite/commande | contenu = donnée ; ACL | RT-02 ; ADV-002 M6 | pas un LLM génératif dans le banc |
| Identité → retrieval | utilisateur autre périmètre | fuite document | C2 confidentialité | droits avant score | RT-05 ; MIG-ACL-01 | rôle ≠ auth prod |
| Outil → réponse | source compromise | donnée contradictoire | C7 qualité | structuré prime ; exposer conflit | ADV-006 / SCN-022 | |
| Question → agent | utilisateur malveillant | injection directe | C2 permissions | refus avant outil | RT-01 ; ADV-001 | |
| Index actif | opérateur / panne | corruption / DoS | C7 dispo | fail-closed + rollback JSON | lab corruption ; MIG-RB-01 | |
| Feedback | auteur / attaquant | PII / consigne | C2 données | classe `risque` | ADV-008 qualify | |
| Planificateur LLM | fournisseur / prompt | ID inventé / outil hors liste | C2/C7 | allowlist + `identifiant_invente` | tests candidat M6 | HF non mesuré en campagne |
| Boucle agent | question répétitive | coût / DoS | C7 budget | max_repeated_calls | ADV-004 | |
| Document prioritaire | empoisonnement | priorité illicite | C2 | pas de boost politique | RT-03/04 | |
| Extraction | opérateur traces | secret dans sortie | C2 | forbidden_fields traces | RT-07 ; policy M6 | |

Inclure explicitement : empoisonnement, priorité malveillante, extraction, boucle coûteuse, déni de service — couverts RT-03…09.
