"""
OpenRouter API client for Gemini 2.5 Pro audio analysis.
Sends audio files + prompts, gets structured JSON responses.
Requires OPENROUTER_API_KEY env var.
"""

import base64
import json
import mimetypes
import os
import re
import time
from pathlib import Path
from typing import Optional
from urllib import request, error


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# Gemini handles the audio analysis because Claude has no audio input; pin the
# stable GA model id (not a "-preview" alias) so the pipeline stays reproducible.
MODEL = "google/gemini-2.5-pro"
MAX_RETRIES = 3
TIMEOUT_SECONDS = 120

# Approximate pricing per million tokens (USD) — Gemini 2.5 Pro via OpenRouter
COST_PER_M_INPUT = 2.50
COST_PER_M_OUTPUT = 15.00


def _get_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise EnvironmentError(
            "OPENROUTER_API_KEY environment variable is not set. "
            "Get a key at https://openrouter.ai/keys"
        )
    return key


def _audio_mime_type(audio_path: str) -> str:
    """Determine MIME type for an audio file."""
    mime, _ = mimetypes.guess_type(audio_path)
    if mime and mime.startswith("audio/"):
        return mime
    ext_map = {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".flac": "audio/flac",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".aac": "audio/aac",
        ".webm": "audio/webm",
        ".opus": "audio/opus",
    }
    ext = Path(audio_path).suffix.lower()
    return ext_map.get(ext, "audio/mpeg")


def _encode_audio(audio_path: str) -> tuple[str, str]:
    """Read and base64-encode an audio file. Returns (base64_data, mime_type)."""
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {audio_path}")

    mime = _audio_mime_type(audio_path)
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("ascii")
    return data, mime


def _strip_markdown_json(text: str) -> str:
    """Strip markdown code block wrappers that Gemini sometimes adds around JSON."""
    stripped = text.strip()
    # Match ```json ... ``` or ``` ... ```
    match = re.match(r"^```(?:json)?\s*\n?(.*?)\n?\s*```$", stripped, re.DOTALL)
    if match:
        return match.group(1).strip()
    return stripped


def _parse_json_response(text: str) -> dict:
    """Parse JSON from response text, handling markdown wrappers."""
    cleaned = _strip_markdown_json(text)
    return json.loads(cleaned)


def _estimate_cost(usage: dict) -> dict:
    """Estimate cost from token usage."""
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)

    input_cost = (prompt_tokens / 1_000_000) * COST_PER_M_INPUT
    output_cost = (completion_tokens / 1_000_000) * COST_PER_M_OUTPUT
    total_cost = input_cost + output_cost

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(total_cost, 6),
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
    }


def _make_request(payload: dict) -> dict:
    """Send a request to OpenRouter with retry logic and exponential backoff."""
    api_key = _get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/style-genome-analyzer",
        "X-Title": "Style Genome Analyzer",
    }
    body = json.dumps(payload).encode("utf-8")

    last_exception = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = request.Request(
                OPENROUTER_URL,
                data=body,
                headers=headers,
                method="POST",
            )
            with request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                raw = resp.read().decode("utf-8")
                result = json.loads(raw)

            # Check for API-level errors
            if "error" in result:
                err = result["error"]
                msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
                raise RuntimeError(f"OpenRouter API error: {msg}")

            # Print cost estimate
            if "usage" in result:
                cost = _estimate_cost(result["usage"])
                print(
                    f"[OpenRouter] Tokens: {cost['prompt_tokens']} in / "
                    f"{cost['completion_tokens']} out | "
                    f"Cost: ~${cost['estimated_cost_usd']:.4f}"
                )

            return result

        except error.HTTPError as e:
            last_exception = e
            response_body = ""
            try:
                response_body = e.read().decode("utf-8")
            except Exception:
                pass

            # Don't retry on client errors (except 429 rate limit)
            if e.code < 500 and e.code != 429:
                raise RuntimeError(
                    f"OpenRouter HTTP {e.code}: {response_body or e.reason}"
                ) from e

            print(
                f"[OpenRouter] Attempt {attempt}/{MAX_RETRIES} failed "
                f"(HTTP {e.code}). Retrying..."
            )

        except error.URLError as e:
            last_exception = e
            print(
                f"[OpenRouter] Attempt {attempt}/{MAX_RETRIES} failed "
                f"(connection error: {e.reason}). Retrying..."
            )

        except TimeoutError as e:
            last_exception = e
            print(
                f"[OpenRouter] Attempt {attempt}/{MAX_RETRIES} timed out "
                f"after {TIMEOUT_SECONDS}s. Retrying..."
            )

        if attempt < MAX_RETRIES:
            backoff = 2 ** (attempt - 1) * 2  # 2s, 4s
            print(f"[OpenRouter] Waiting {backoff}s before retry...")
            time.sleep(backoff)

    raise RuntimeError(
        f"OpenRouter request failed after {MAX_RETRIES} attempts. "
        f"Last error: {last_exception}"
    )


def analyze_audio(
    audio_path: str,
    prompt: str,
    technical_data: Optional[dict] = None,
) -> dict:
    """
    Send an audio file to Gemini 2.5 Pro for analysis.

    Args:
        audio_path: Path to the audio file (mp3, wav, flac, etc.)
        prompt: Analysis prompt / instructions
        technical_data: Optional dict of pre-extracted technical features
                       (tempo, key, spectral data, etc.) to include in the prompt

    Returns:
        Parsed JSON dict from the model's response
    """
    audio_b64, mime = _encode_audio(audio_path)

    # Build the user message content parts
    content_parts = []

    # Audio goes first so the model "hears" it before reading instructions
    content_parts.append({
        "type": "input_audio",
        "input_audio": {
            "data": audio_b64,
            "format": mime.split("/")[-1],  # e.g., "mpeg", "wav"
        },
    })

    # Build the text prompt
    text = prompt
    if technical_data:
        tech_block = json.dumps(technical_data, indent=2)
        text = (
            f"{prompt}\n\n"
            f"Pre-extracted technical analysis data (use as additional context):\n"
            f"```json\n{tech_block}\n```"
        )

    content_parts.append({"type": "text", "text": text})

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional music analyst. Respond ONLY with valid JSON. "
                    "No markdown wrappers, no explanatory text outside the JSON object. "
                    "If the analysis requires subjective judgment, still structure it as JSON."
                ),
            },
            {
                "role": "user",
                "content": content_parts,
            },
        ],
        "temperature": 0.3,
        "max_tokens": 8192,
        "response_format": {"type": "json_object"},
    }

    result = _make_request(payload)

    # Extract the response text
    choices = result.get("choices", [])
    if not choices:
        raise RuntimeError("OpenRouter returned no choices in response")

    text_response = choices[0].get("message", {}).get("content", "")
    if not text_response:
        raise RuntimeError("OpenRouter returned empty response content")

    return _parse_json_response(text_response)


def generate_text(prompt: str) -> str:
    """
    Send a text-only prompt to Gemini 2.5 Pro.

    Args:
        prompt: The text prompt

    Returns:
        Raw text response from the model
    """
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.5,
        "max_tokens": 4096,
    }

    result = _make_request(payload)

    choices = result.get("choices", [])
    if not choices:
        raise RuntimeError("OpenRouter returned no choices in response")

    return choices[0].get("message", {}).get("content", "")


if __name__ == "__main__":
    # Quick self-test: verify API key is set and model is reachable
    print("Style Genome Analyzer — OpenRouter Client")
    print(f"Model: {MODEL}")
    print(f"Endpoint: {OPENROUTER_URL}")

    try:
        _get_api_key()
        print("API key: OK")
    except EnvironmentError as e:
        print(f"API key: MISSING — {e}")
        exit(1)

    print("\nSending test prompt...")
    try:
        response = generate_text(
            "Respond with exactly: {\"status\": \"ok\", \"model\": \"gemini-2.5-pro\"}"
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
