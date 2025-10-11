from __future__ import annotations

from typing import Any, Dict, Optional

import os
from pathlib import Path

_ENV_LOADED = False


def _load_env_file_once() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    _ENV_LOADED = True
    try:
        # Look for .env in CWD
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                # Don't overwrite if already set
                if key and (key not in os.environ):
                    os.environ[key] = val
    except Exception:
        # Fail silently; fallback to normal env/secrets
        pass


def _get_api_key() -> Optional[str]:
    _load_env_file_once()
    # Prefer Streamlit secrets when available
    try:
        import streamlit as st  # type: ignore

        val = st.secrets.get("GROQ_API_KEY")  # type: ignore[attr-defined]
        if isinstance(val, str) and val.strip():
            return val.strip()
    except Exception:
        pass

    # Fallback to environment variable
    key = os.environ.get("GROQ_API_KEY", "").strip()
    return key or None


def groq_available() -> bool:
    return _get_api_key() is not None


def chat_with_groq(
    user_message: str,
    *,
    model: str = "openai/gpt-oss-20b",
    temperature: float = 0.6,
    max_completion_tokens: int = 1024,
    include_reasoning: Optional[bool] = None,
    reasoning_format: Optional[str] = None,
    reasoning_effort: Optional[str] = None,
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Returns (answer, reasoning, error). Uses OpenAI-compatible Groq endpoint.
    """
    api_key = _get_api_key()
    if not api_key:
        return None, None, "GROQ_API_KEY chưa được cấu hình (secrets hoặc biến môi trường)."

    try:
        import requests  # type: ignore
    except Exception:
        return None, None, "Thiếu thư viện 'requests'. Hãy cài đặt trong requirements.txt."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": user_message}],
        "temperature": float(temperature),
        "max_completion_tokens": int(max_completion_tokens),
        "stream": False,
    }

    # Apply reasoning options based on docs
    if include_reasoning is not None:
        payload["include_reasoning"] = bool(include_reasoning)
    if reasoning_format is not None:
        payload["reasoning_format"] = str(reasoning_format)
    if reasoning_effort is not None:
        payload["reasoning_effort"] = str(reasoning_effort)

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code >= 400:
            return None, None, f"Groq API lỗi {resp.status_code}: {resp.text[:500]}"
        data = resp.json()
    except Exception as exc:  # Network/parse errors
        return None, None, f"Không gọi được Groq API: {exc}"

    try:
        choice = data["choices"][0]
        message = choice.get("message", {})
        content = message.get("content")
        # GPT-OSS may return reasoning in 'reasoning'; other models may use formatting
        reasoning = message.get("reasoning")
        return str(content) if content is not None else None, reasoning, None
    except Exception:
        return None, None, "Phản hồi Groq không hợp lệ."
