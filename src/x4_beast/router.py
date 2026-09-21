from .audit import AuditStore
from .providers.base import ProviderError, ProviderResponse
from .providers.registry import build_registry

class ModelRouter:
    def __init__(self, settings, audit: AuditStore):
        self.providers = build_registry(settings)
        self.audit = audit

    async def chat(self, messages, preferred=None, model=None) -> ProviderResponse:
        names = [preferred] if preferred else [
            "ollama", "openai", "openrouter", "groq", "mistral", "nvidia", "gemini"
        ]
        errors = []
        for name in names:
            if not name or name not in self.providers:
                continue
            try:
                result = await self.providers[name].chat(messages, model)
                self.audit.write({
                    "event": "provider_call",
                    "provider": result.provider,
                    "model": result.model,
                    "status": "success",
                    "latency_ms": result.latency_ms,
                })
                return result
            except ProviderError as exc:
                errors.append(str(exc))
                self.audit.write({
                    "event": "provider_call",
                    "provider": name,
                    "status": "error",
                    "error": str(exc),
                })
        raise RuntimeError("No provider succeeded: " + " | ".join(errors))
