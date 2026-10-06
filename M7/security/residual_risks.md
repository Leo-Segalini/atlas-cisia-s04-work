# Risques résiduels — M7

**Date :** 2026-10-06

| ID | Risque | Gravité | Traitement | Preuve / limite |
|---|---|---|---|---|
| RR-01 | LLM cloud planificateur (transfert, suggestion maligne) | majeur | accepter labo / heuristique par défaut ; ne pas promouvoir HF | veille ; pas de campagne LLM |
| RR-02 | Rôle banc ≠ authentification | majeur | documenter ; bloquer prod | data_policy |
| RR-03 | Absence d'échec ≠ absence de vulnérabilité LLM | majeur | accepter | red_team limit |
| RR-04 | Échecs starter `m6_for_m7` si on repart de la référence | majeur | utiliser état personnel M6 ou re-corriger | README m6_for_m7 |
| RR-05 | Outil à effet un jour mal branché | bloquant si réel | executable=false ; hors chemin ref | ADR-0002 |
| RR-06 | Rétention 30 j insuffisante hors POC | mineur | question M8 | passage veille |
| RR-07 | Parité lexicale ≠ qualité génération | mineur | accepter | lab limitations |
| RR-08 | Revue indépendante non signée formateur | majeur process | pending signature | independent_review.md |

Aucun risque **bloquant ouvert** sur le chemin lecture seule labo. RR-05 reste bloquant pour toute activation réelle d'effet.
