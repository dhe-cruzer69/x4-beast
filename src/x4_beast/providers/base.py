from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ProviderResponse:
    provider: str
    model: str
    content: str
    latency_ms: int

class ProviderError(RuntimeError):
    pass

class Provider(ABC):
    name: str

    @abstractmethod
    async def chat(self, messages: list[dict[str, str]], model: str | None = None) -> ProviderResponse:
        raise NotImplementedError
