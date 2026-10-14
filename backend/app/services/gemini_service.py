"""
Gemini Service — Asynchronous Google Gemini 1.5 Flash Model Integration
"""

import os
import httpx
from typing import Optional


async def query_gemini_api(
    system_prompt: str,
    user_prompt: str,
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
) -> Optional[str]:
    """
    Asynchronously queries Google Gemini 1.5 Flash generateContent API.
    Returns generated candidate text or None if call fails or key is missing.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None

    endpoint = api_url or os.environ.get(
        "GEMINI_API_URL",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}",
    )
    if "?key=" not in endpoint and "&key=" not in endpoint:
        endpoint = f"{endpoint}?key={key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt},
                    {"text": user_prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1000,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(endpoint, json=payload)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"]
    except Exception as e:
        print(f"[Gemini Service Warning] Failed to reach Gemini API: {e}")
        return None

    return None
