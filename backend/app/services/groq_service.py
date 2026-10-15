"""
Groq AI Service — High-Performance Llama-3.3 / Llama-3.1 Inference Integration
Supports OpenAI-compatible Chat Completions and Native Tool Calling.
Official endpoint: https://api.groq.com/openai/v1/chat/completions
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("groq_service")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"


def get_groq_api_key() -> Optional[str]:
    """Retrieves the configured Groq API key from environment."""
    return os.environ.get("GROQ_API_KEY")


def get_groq_model() -> str:
    """Retrieves the configured Groq model name."""
    return os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL)


def is_groq_configured() -> bool:
    """Checks whether a valid Groq API key is present."""
    key = get_groq_api_key()
    return bool(key and key.strip())


async def call_groq_chat(
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: str = "auto",
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
    api_key: Optional[str] = None,
    timeout_seconds: float = 20.0,
) -> Optional[Dict[str, Any]]:
    """
    Asynchronously calls Groq's OpenAI-compatible Chat Completions API.
    Supports tool calling when tools list is provided.

    Returns dict with keys:
        'text': Optional[str]
        'tool_calls': List[Dict[str, Any]] (if model called tools)
        'model': str
        'finish_reason': str
    Returns None if request fails, key is missing, or rate limits are hit.
    """
    key = api_key or get_groq_api_key()
    if not key or not key.strip():
        logger.debug("Groq API key not configured. Using deterministic fallback.")
        return None

    target_model = model or get_groq_model()

    payload: Dict[str, Any] = {
        "model": target_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = tool_choice

    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "NIAT-ParentTrust-AI/2.5.0",
    }

    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})
                finish_reason = choice.get("finish_reason", "")

                text_content = message.get("content") or ""
                tool_calls = message.get("tool_calls") or []

                # Normalize raw_message: Groq rejects null content in conversation
                # history when sending follow-up requests after tool calls.
                safe_raw_message = {
                    "role": message.get("role", "assistant"),
                    "content": text_content,  # always a string, never None
                }
                if tool_calls:
                    safe_raw_message["tool_calls"] = tool_calls

                return {
                    "text": text_content,
                    "tool_calls": tool_calls,
                    "model": data.get("model", target_model),
                    "finish_reason": finish_reason,
                    "raw_message": safe_raw_message,
                }
            elif response.status_code == 401:
                logger.warning("[Groq Service] 401 Unauthorized: Invalid GROQ_API_KEY provided.")
                return None
            elif response.status_code == 429:
                logger.warning("[Groq Service] 429 Rate Limit exceeded on Groq API tier.")
                return None
            elif response.status_code == 400:
                err_text = response.text[:200]
                logger.warning(f"[Groq Service] 400 Bad Request: {err_text}")
                return None
            else:
                logger.warning(f"[Groq Service] Unexpected status {response.status_code}: {response.text[:200]}")
                return None

    except httpx.TimeoutException:
        logger.warning(f"[Groq Service] Request timed out after {timeout_seconds}s.")
        return None
    except httpx.RequestError as e:
        logger.warning(f"[Groq Service] Network error connecting to Groq API: {e}")
        return None
    except Exception as e:
        logger.warning(f"[Groq Service] Unexpected exception calling Groq: {e}")
        return None
