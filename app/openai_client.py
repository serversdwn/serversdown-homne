from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict, List

from fastapi import HTTPException

try:
    from openai import OpenAI
except ModuleNotFoundError as exc:  # pragma: no cover - optional dependency
    raise RuntimeError(
        "The 'openai' package is required for ingredient recognition. Install it via 'pip install openai'."
    ) from exc

MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")


def encode_image(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")


def request_ingredient_list(image_b64: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are helping a family catalogue ingredients in their fridge. "
                            "Return a JSON object with an 'items' array. Each item must have "
                            "a 'name', optional 'amount', and optional 'location'. The JSON should be easy for software to parse."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image": {"base64": image_b64},
                    },
                ],
            }
        ],
        max_output_tokens=600,
    )

    for item in response.output:
        if item.type == "output_text":
            text = item.text
            break
    else:  # pragma: no cover - defensive fallback
        raise HTTPException(status_code=500, detail="Unexpected response format from vision model.")

    try:
        parsed: Dict[str, Any] = json.loads(text)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail="Vision model returned output that could not be parsed as JSON.",
        ) from exc

    items: List[Dict[str, Any]] = parsed.get("items", [])
    if not isinstance(items, list):
        raise HTTPException(status_code=500, detail="Vision model returned items in an unexpected format.")

    return {"items": items, "raw_text": text}
