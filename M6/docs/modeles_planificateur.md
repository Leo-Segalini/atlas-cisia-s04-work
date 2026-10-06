# Planificateurs modèle — M6

Le **registre** et la **politique** restent la loi. Le planificateur ne fait que
**proposer** le prochain outil.

## Modes

| Mode | Variable | Dépendance | Usage |
|---|---|---|---|
| Heuristique (défaut) | `DIAGOPS_PLANNER=heuristic` | aucune | tests, gates, CI |
| Ollama (local) | `DIAGOPS_PLANNER=ollama` | Ollama + modèle | labo offline |
| Hugging Face (cloud) | `DIAGOPS_PLANNER=huggingface` | `HF_TOKEN` | labo avec réseau |

## Configuration

Fichier exemple : `.env.example` à la racine de `work/M6/`.

```bash
# Heuristique (recommandé pour mesurer)
export DIAGOPS_PLANNER=heuristic

# Ollama
export DIAGOPS_PLANNER=ollama
export OLLAMA_HOST=http://127.0.0.1:11434
export DIAGOPS_OLLAMA_MODEL=qwen2.5:7b-instruct
ollama pull qwen2.5:7b-instruct

# Hugging Face
export DIAGOPS_PLANNER=huggingface
export HF_TOKEN=hf_...
export DIAGOPS_HF_MODEL=Qwen/Qwen2.5-7B-Instruct
```

Puis :

```bash
python3 eval/run_agent_eval.py --output results/eval_planner.json
```

## Garde-fous

1. La suggestion LLM hors liste blanche est **ignorée** (fallback heuristique).
2. Budget, timeouts, `stop_on_tool_error` s'appliquent toujours.
3. Un échec réseau / token manquant → fallback heuristique (pas de crash).
4. Les traces ne stockent pas le prompt complet ni le raisonnement privé.
5. Pour une comparaison chiffrée du brief : toujours mesurer en `heuristic`.

## Fichiers

- `agent/providers.py` — `HeuristicPlanner`, `OllamaPlanner`, `HuggingFacePlanner`, `build_planner`
- `agent/runner.py` — injecte le planificateur dans `BoundedAgent`
