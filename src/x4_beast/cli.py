import typer
import uvicorn
from .config import Settings
from .api import create_app

app = typer.Typer(help="X4 BEAST CLI")

@app.command()
def doctor():
    settings = Settings()
    print("X4 BEAST doctor")
    print(f"ollama: {settings.ollama_base_url}")
    print(f"ollama_model: {settings.ollama_model}")
    print(f"openai: {'configured' if settings.openai_api_key else 'not configured'}")
    print(f"openrouter: {'configured' if settings.openrouter_api_key else 'not configured'}")
    print(f"groq: {'configured' if settings.groq_api_key else 'not configured'}")
    print(f"mistral: {'configured' if settings.mistral_api_key else 'not configured'}")
    print(f"nvidia: {'configured' if settings.nvidia_api_key else 'not configured'}")
    print(f"gemini: {'configured' if settings.gemini_api_key else 'not configured'}")

@app.command()
def serve(host: str | None = None, port: int | None = None):
    settings = Settings()
    uvicorn.run(
        create_app(),
        host=host or settings.host,
        port=port or settings.port,
    )

if __name__ == "__main__":
    app()
