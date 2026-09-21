from fastapi import FastAPI
from .agent import Agent
from .audit import AuditStore
from .config import Settings
from .mcp_manager import MCPManager
from .models import AgentRequest, ChatRequest, ChatResponse
from .policy import PolicyEngine
from .router import ModelRouter

def create_app() -> FastAPI:
    settings = Settings()
    settings.ensure_data_dirs()
    audit = AuditStore(settings.audit_jsonl)
    router = ModelRouter(settings, audit)
    policy = PolicyEngine()
    mcp = MCPManager()
    agent = Agent(router, policy, audit)
    app = FastAPI(title="X4 BEAST", version="0.1.1")

    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "providers": sorted(router.providers),
            "mcp_servers": mcp.summary(),
        }

    @app.post("/v1/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.message})
        result = await router.chat(messages, request.provider, request.model)
        return ChatResponse(
            provider=result.provider,
            model=result.model,
            content=result.content,
            trace_id=audit.write({"event": "chat", "provider": result.provider})["event_id"],
        )

    @app.post("/v1/agent/run")
    async def run_agent(request: AgentRequest):
        return await agent.run(
            request.message,
            request.max_steps,
            request.provider,
        )

    return app

app = create_app()
