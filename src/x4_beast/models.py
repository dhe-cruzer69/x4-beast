from typing import Any, Literal
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    provider: str | None = None
    model: str | None = None
    system: str | None = None

class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)

class ToolResult(BaseModel):
    name: str
    decision: str
    output: Any = None
    error: str | None = None

class AgentRequest(BaseModel):
    message: str = Field(min_length=1)
    provider: str | None = None
    model: str | None = None
    max_steps: int = Field(default=5, ge=1, le=20)

class ChatResponse(BaseModel):
    provider: str
    model: str
    content: str
    trace_id: str
