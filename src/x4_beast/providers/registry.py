from .base import Provider
from .gemini import GeminiProvider
from .openai_compatible import OpenAICompatibleProvider
from ..config import Settings

def build_registry(settings: Settings) -> dict[str, Provider]:
    return {
        "ollama": OpenAICompatibleProvider(
            "ollama",
            settings.ollama_base_url,
            None,
            settings.ollama_model,
        ),
        "openai": OpenAICompatibleProvider(
            "openai",
            "https://api.openai.com/v1",
            settings.openai_api_key,
            settings.openai_model,
        ),
        "openrouter": OpenAICompatibleProvider(
            "openrouter",
            "https://openrouter.ai/api/v1",
            settings.openrouter_api_key,
            settings.openrouter_model,
            {
                "HTTP-Referer": settings.openrouter_site_url or "",
                "X-Title": settings.openrouter_app_name,
            },
        ),
        "groq": OpenAICompatibleProvider(
            "groq",
            "https://api.groq.com/openai/v1",
            settings.groq_api_key,
            settings.groq_model,
        ),
        "mistral": OpenAICompatibleProvider(
            "mistral",
            "https://api.mistral.ai/v1",
            settings.mistral_api_key,
            settings.mistral_model,
        ),
        "nvidia": OpenAICompatibleProvider(
            "nvidia",
            "https://integrate.api.nvidia.com/v1",
            settings.nvidia_api_key,
            settings.nvidia_model,
        ),
        "gemini": GeminiProvider(settings.gemini_api_key, settings.gemini_model),
    }
