# Journal de veille DiagOps — M6

> Ce journal n'est **pas** un avis juridique.

## Relais reçu (M5)

- Source : `work/M5/veille_diagops/passage_m6.md` et `data_pack/.../m5_for_m6/veille_diagops/journal.md`
- Points ouverts transmis : qualification AI Act, rétention traces, fournisseur cloud, feedback ≠ label automatique.

---

## Entrée M6 — 2026-09-21

### Consultation

| Élément | Détail |
|---|---|
| Date | 2026-09-21 |
| Responsable | Apprenant DiagOps S04 (`work/M6`) |
| Sources | Règlement (UE) 2024/1689 (AI Act) — EUR-Lex CELEX `32024R1689` ; principes CNIL sur IA et données (minimisation, pas de réemploi non maîtrisé des retours) ; relais M5 |

### Analyse

1. L'agent M6 reste **lecture seule**, multi-outils mais **borné** (budget, allowlist). Ce n'est pas une autonomie opérationnelle.
2. Le feedback humain crée un **traitement potentiel** (commentaires, parfois PII) : la classe `risque` et l'interdiction d'export d'entraînement sont des contrôles minimaux.
3. Brancher un LLM cloud (HF) ajoute localisation / sous-traitance — hors cadrage « labo local » tant qu'aucune DPA / décision n'est écrite.

### Décision de veille

**L'autonomie bornée et le feedback qualifié ne lèvent pas la supervision humaine.**  
Toute promotion reste une décision nominative ; aucun apprentissage automatique depuis le CSV brut.

### Traduction dans un contrôle déjà spécifié

| Contrôle | Traduction veille |
|---|---|
| `treat_tool_output_as_data: true` | contenu outil ≠ instruction (INV-08, ADV-002) |
| classe `risque` feedback | exclusion PII / instructions — jamais d'entraînement |
| `docs/decision_promotion.md` = **`prolonger`** | refus de promotion automatique (INV-07) |

### Questions transmises à M7

Voir `veille_diagops/passage_m7.md`.
