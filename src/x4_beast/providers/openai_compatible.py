import time
import httpx
from .base import Provider, ProviderError, ProviderResponse

class OpenAICompatibleProvider(Provider):
    def __init__(
        self,
        name: str,
        base_url: str,
        api_key: str | None,
        default_model: str,
        headers: dict[str, str] | None = None,
    ):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.default_model = default_model
        self.headers = headers or {}

    async def chat(self, messages, model=None):
        if not self.api_key and self.name != "ollama":
            raise ProviderError(f"{self.name}: API key not configured")
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": 0.2,
        }
        headers = {"content-type": "application/json", **self.headers}
        if self.api_key:
            headers["authorization"] = f"Bearer {self.api_key}"
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise ProviderError(f"{self.name}: {exc}") from exc
        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"{self.name}: unexpected response schema") from exc
        return ProviderResponse(
            provider=self.name,
            model=payload["model"],
            content=content,
            latency_ms=int((time.perf_counter() - start) * 1000),
        )
