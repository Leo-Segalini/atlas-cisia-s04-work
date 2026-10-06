# Alternatives local / cloud / hybride — M7

**Date :** 2026-10-06

| Couche | Local | Cloud | Hybride | Recommandation labo |
|---|---|---|---|---|
| Génération / plan | heuristic / Ollama | HF Inference | heuristic + HF secours | **local heuristic** pour gates |
| Embeddings | N/A (lexical) | API embed | cache local + API | rester lexical tant que non justifié |
| Index | JSON / SQLite | vector DB managée | SQLite + backup objet | **JSON actif**, SQLite candidat |
| API | process local | SaaS | reverse-proxy | local |
| Traces | fichiers `results/` | SIEM cloud | local + export | local, rétention 30 j |
| Sauvegardes | copie FS checksumée | object storage | les deux | FS + hash |

## Critères

| Critère | Local | Cloud | Hybride |
|---|---|---|---|
| Performance labo | suffisante | variable réseau | variable |
| Coût | ≈ 0 | tokens / seats | mixte |
| Empreinte | machine apprenant | datacenter tiers | mixte |
| Compétences | Python | ops cloud | les deux |
| Disponibilité | machine unique | SLA fournisseur | fallback |
| Localisation | maîtrisée | transfert | partiel |
| Verrou | faible | fort | moyen |
| Réversibilité | haute (prouvé) | basse | moyenne |

**Choix :** architecture **locale** pour le chemin de référence ; cloud LLM seulement expérimental, hors promotion.
