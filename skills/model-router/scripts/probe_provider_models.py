#!/usr/bin/env python3
"""Probe provider model catalogs without printing credentials.

Keys are read from environment variables, DSH's credential references, or a
configured OpenAI-compatible gateway. Only endpoint hosts, status, and model
IDs are printed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request


PROVIDERS = (
    ("deepseek", ("DEEPSEEK_API_KEY",), "https://api.deepseek.com/models"),
    ("glm", ("GLM_API_KEY", "ZHIPU_API_KEY", "BIGMODEL_API_KEY"), "https://open.bigmodel.cn/api/paas/v4/models"),
)


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return values
    for line in lines:
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        name, value = line.split("=", 1)
        values[name.strip()] = value.strip().strip("\"'")
    return values


def dsh_credential(name: str) -> str | None:
    """Read one simple scalar under refs from DSH's credential file."""
    path = Path.home() / ".dsh" / ".credentials.yaml"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    match = re.search(rf"^\s{{2}}{re.escape(name)}:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else None


def resolve_key(names: tuple[str, ...]) -> tuple[str | None, str]:
    for name in names:
        if os.environ.get(name):
            return os.environ[name], f"env:{name}"
        value = dsh_credential(name)
        if value:
            return value, f"dsh-credential:{name}"
    return None, "none"


def request_models(url: str, key: str) -> list[str]:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.load(response)
    models = payload.get("data", []) if isinstance(payload, dict) else []
    return sorted({item.get("id") for item in models if isinstance(item, dict) and item.get("id")})


def probe(name: str, env_keys: tuple[str, ...], url: str) -> dict[str, object]:
    key, credential_source = resolve_key(env_keys)
    if not key:
        return {"provider": name, "status": "key_not_exposed", "credential_source": credential_source, "models": []}
    try:
        ids = request_models(url, key)
        return {"provider": name, "status": "ok", "credential_source": credential_source, "models": ids}
    except urllib.error.HTTPError as exc:
        return {"provider": name, "status": f"http_{exc.code}", "models": []}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"provider": name, "status": f"error:{type(exc).__name__}", "models": []}


def probe_gateway() -> dict[str, object]:
    for config_path in sorted(Path.home().glob(".openclaw-agent-*/openclaw.json")):
        env_path = config_path.parent / ".env"
        env_values = parse_env_file(env_path)
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        config_env = config.get("env", {}).get("vars", {})
        base = config_env.get("OPENCLAW_NEWAPI_BASE_URL") or env_values.get("OPENCLAW_NEWAPI_BASE_URL")
        key = env_values.get("OPENCLAW_NEWAPI_API_KEY")
        if not base or not key or urllib.parse.urlparse(base).scheme != "https":
            continue
        try:
            ids = request_models(base.rstrip("/") + "/models", key)
            selected = [model for model in ids if any(name in model.lower() for name in ("deepseek", "glm"))]
            return {
                "provider": "openai-compatible-gateway",
                "status": "ok",
                "endpoint_host": urllib.parse.urlparse(base).hostname,
                "credential_source": f"env-file:{env_path}",
                "models": selected,
            }
        except urllib.error.HTTPError as exc:
            return {"provider": "openai-compatible-gateway", "status": f"http_{exc.code}", "models": []}
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return {"provider": "openai-compatible-gateway", "status": f"error:{type(exc).__name__}", "models": []}
    return {"provider": "openai-compatible-gateway", "status": "not_configured", "models": []}


def main() -> None:
    results = [probe(*provider) for provider in PROVIDERS]
    results.append(probe_gateway())
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
