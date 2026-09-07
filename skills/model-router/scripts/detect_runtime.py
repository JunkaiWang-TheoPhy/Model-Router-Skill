#!/usr/bin/env python3
"""Report conservative, non-secret model/runtime hints for gpt-router.

This does not prove that a model is callable and never prints token values.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


MODEL_KEYS = ("CODEX_MODEL", "OMX_MODEL", "OPENAI_MODEL", "MODEL")
SUPPORTED_KEYS = ("OMX_SUPPORTED_MODELS", "CODEX_SUPPORTED_MODELS", "OPENAI_MODELS")


def split_models(value: str) -> list[str]:
    return sorted({item.strip() for item in value.replace(",", " ").split() if item.strip()})


def main() -> None:
    current = next((os.environ[key] for key in MODEL_KEYS if os.environ.get(key)), None)
    configured: set[str] = set()
    sources: list[str] = []

    for key in SUPPORTED_KEYS:
        if os.environ.get(key):
            configured.update(split_models(os.environ[key]))
            sources.append(f"env:{key}")

    for key in MODEL_KEYS:
        value = os.environ.get(key)
        if value:
            configured.add(value.strip())
            sources.append(f"env:{key}")

    # Read only model-like scalar values from common local config files.
    for path in (Path.home() / ".codex" / "config.toml", Path.home() / ".codex" / "config.json"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            lowered = line.lower()
            if "=" not in line:
                continue
            key_name = line.split("=", 1)[0].strip().split(".")[-1].lower()
            if key_name not in {"model", "models", "default_model", "supported_models"}:
                continue
            if "key" in lowered or "token" in lowered:
                continue
            value = line.split("=", 1)[1].strip().strip(",\"'")
            if value.startswith("["):
                value = value.strip("[]")
                configured.update(split_models(value.replace('"', "").replace("'", "")))
            elif value and len(value) < 120 and " " not in value:
                configured.add(value)
            sources.append(f"config:{path}")

    result: dict[str, Any] = {
        "current_model": current or "unknown",
        "known_supported_models": sorted(configured),
        "evidence_sources": sorted(set(sources)),
        "notes": [
            "Current model is unknown unless runtime metadata exposes it.",
            "Configured or listed models are not guaranteed callable on this host.",
            "No secret values are emitted.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
