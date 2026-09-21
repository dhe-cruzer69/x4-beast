import time
import httpx
from .base import Provider, ProviderError, ProviderResponse

class GeminiProvider(Provider):
    name = "gemini"

    def __init__(self, api_key: str | None, default_model: str):
        self.api_key = api_key
        self.default_model = default_model

    async def chat(self, messages, model=None):
        if not self.api_key:
            raise ProviderError("gemini: API key not configured")
        model = model or self.default_model
        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent"
        )
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.post(
                    url,
                    params={"key": self.api_key},
                    json={"contents": contents},
                )
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise ProviderError(f"gemini: {exc}") from exc
        data = response.json()
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("gemini: unexpected response schema") from exc
        return ProviderResponse(
            provider=self.name,
            model=model,
            content=text,
            latency_ms=int((time.perf_counter() - start) * 1000),
        )
