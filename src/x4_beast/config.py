from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8787
    db: str = "./data/x4.db"
    audit_jsonl: str = "./data/audit.jsonl"

    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2:3b"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-4.1-mini"
    openrouter_site_url: str | None = None
    openrouter_app_name: str = "X4-BEAST"

    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"

    mistral_api_key: str | None = None
    mistral_model: str = "mistral-small-latest"

    nvidia_api_key: str | None = None
    nvidia_model: str = "meta/llama-3.1-8b-instruct"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="X4_",
        extra="ignore",
    )

    def ensure_data_dirs(self) -> None:
        Path(self.db).parent.mkdir(parents=True, exist_ok=True)
        Path(self.audit_jsonl).parent.mkdir(parents=True, exist_ok=True)
