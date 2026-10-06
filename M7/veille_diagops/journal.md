# Journal de veille DiagOps — M7

> Pas un avis juridique.

## Relais reçu (M6)

`work/M6/veille_diagops/passage_m7.md` — supervision humaine maintenue ; 3 questions ouvertes (cloud LLM, rétention, signataire promotion).

---

## Entrée M7 — 2026-10-06

### Consultation

| Élément | Détail |
|---|---|
| Date | 2026-10-06 |
| Sources | Règlement (UE) 2024/1689 (AI Act) EUR-Lex CELEX `32024R1689` ; relais M5/M6 ; principes minimisation données |
| Périmètre | architecture cible, index SQLite candidat, outil à effet **simulé** |

### Analyse

1. L'outil `request_inspection_simulated` (`executable: false`) **ne modifie pas** à lui seul une qualification « haut risque » industrielle : aucun effet réel, bac à sable tabletop.
2. Une option **cloud** LLM sur le chemin critique augmenterait les questions de transfert et de supervision — **écartée** du chemin de référence (ADR-0001).
3. Exigences cybersécurité / traçabilité : checksums export, traces bornées, promotion humaine — déjà dans gates cibles.

### Décision

**Maintenir supervision humaine et lecture seule sur le chemin de référence.**  
Différer tout effet réel et toute bascule d'index actif. Traduction : ADR-0001/0002, `residual_risks.md`, `architecture/target.md` (décision différer).

### Questions → M8

Voir `handoff_m8.md`.
