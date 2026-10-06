"""Clients HTTP optionnels pour planificateurs LLM (hors agent/tools scannés).

Ce module est volontairement hors de `agent/` et `tools/` : le test
d'absence d'effet externe refuse urllib/requests dans ces dossiers.
Les adaptateurs d'outils restent en lecture seule sur le data pack.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any


def extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else None
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        try:
            value = json.loads(match.group(0))
            return value if isinstance(value, dict) else None
        except json.JSONDecodeError:
            return None


def ollama_generate(*, prompt: str, model: str, base_url: str, timeout_s: float) -> str:
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0},
    }).encode()
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_s) as response:
        payload = json.loads(response.read().decode())
    return str(payload.get("response", ""))


def huggingface_chat(*, system: str, user: str, model: str, token: str, endpoint: str, timeout_s: float) -> str:
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }).encode()
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_s) as response:
        payload = json.loads(response.read().decode())
    return str(payload["choices"][0]["message"]["content"])


def default_hf_endpoint() -> str:
    return os.environ.get(
        "DIAGOPS_HF_URL",
        "https://router.huggingface.co/v1/chat/completions",
    )
