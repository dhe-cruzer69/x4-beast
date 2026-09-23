# X4 BEAST

**Local-first, provider-agnostic AI agent infrastructure** with policy controls, MCP, model routing, audit, autofixing, and the 7-capability autonomous agent architecture.

> The system should never equate execution with success.

**Current version:** `0.2.0` (Beast Mode)  
**Status:** Active development • Hybrid local/cloud • Autofix enabled under policy

---

## Beast Mode Features (v0.2)

| Feature | Description |
|---------|-------------|
| **Hybrid Local/Cloud** | Prefer local (Ollama) → automatic policy-controlled cloud fallback |
| **Autofixing Tools** | Detect failures → propose patches → apply only when authorized by policy |
| **Evidence-First Loop** | Every action produces an evidence receipt (`OBSERVED` → `VALIDATED` / `UNKNOWN`) |
| **Policy-Gated Autonomy** | Levels 0–3 (Observe → Assist → Governed Autopilot → Never) |
| **MCP Native** | First-class Model Context Protocol support via x4-mcp |
| **Intelligent Routing** | Capability / cost / latency / reliability scoring (x4-router-score) |
| **Secure by Default** | Deny-by-default tools, sandbox, least privilege, secret isolation |
| **Observability** | Structured telemetry + evidence receipts (x4-obs) |

---

## The 7 Capabilities

| # | Capability | Core mechanism | Success criterion |
|---|------------|----------------|-------------------|
| 1 | Reliable autonomous execution | Planner + executor + retry/recovery + autofix | Goal completed across multiple tools |
| 2 | Verification before success | Tests + output inspection + evidence ledger | No PASS without evidence |
| 3 | Secure tools & credentials | Sandbox + least privilege + secret isolation + policy gates | Unsafe actions blocked |
| 4 | Persistent context & memory | State store + project memory + task history | Agent resumes work correctly |
| 5 | Multi-agent orchestration | Delegation + specialist agents + coordinator | Complex tasks decomposed effectively |
| 6 | Intelligent routing | Capability/cost/latency/reliability router | Best available model/tool selected dynamically |
| 7 | Human-in-the-loop control | Approval gates + uncertainty states + escalation | High-impact actions require human approval |

```text
INTENT → PLAN → POLICY → EXECUTE → OBSERVE → VERIFY → EVIDENCE
                                                      │
                                         ┌────────────┼────────────┐
                                         ▼            ▼            ▼
                                       PASS        UNKNOWN        FAIL
                                         │            │            │
                                      RELEASE    HUMAN REVIEW   RECOVER / AUTOFIX
```

---

## Quick Start

### Manual

```bash
git clone https://github.com/dhe-cruzer69/x4-beast.git
cd x4-beast

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
cp .env.example .env
# Edit .env — add only the keys you actually use

python -m x4_beast doctor          # Check providers & health
python -m x4_beast serve           # Start API on http://127.0.0.1:8787
```

### One-command (recommended)

```bash
chmod +x scripts/start.sh
./scripts/start.sh                 # background + logs to data/x4-beast.log
./scripts/stop.sh                  # stop later
```

### Docker (fully isolated)

```bash
docker compose up -d --build
docker compose logs -f
docker compose down
```

Container uses `restart: unless-stopped`.

### systemd (Linux — starts on boot)

```bash
sudo cp deploy/x4-beast.service /etc/systemd/system/
# Edit paths if needed (default /opt/x4-beast)
sudo systemctl daemon-reload
sudo systemctl enable --now x4-beast
sudo systemctl status x4-beast
```

---

## Environment Variables

Copy `.env.example` → `.env`:

```env
X4_HOST=127.0.0.1
X4_PORT=8787
X4_AUTONOMY_LEVEL=1          # 0=Observe, 1=Assist, 2=Governed Autopilot
X4_AUTOFIX_ENABLED=true      # only applies inside policy bounds

# Local (preferred)
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b

# Cloud fallback (optional)
OPENAI_API_KEY=
OPENROUTER_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
NVIDIA_API_KEY=
GEMINI_API_KEY=
```

Router always tries **Ollama first**. Cloud is used only as policy-approved fallback.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health + available providers |
| POST | `/v1/chat` | Simple chat |
| POST | `/v1/agent/run` | Full agent loop with tools + policy + evidence |
| POST | `/v1/autofix` | Propose / apply autofix (policy gated) |

Example:

```bash
curl -X POST http://127.0.0.1:8787/v1/chat \
  -H "content-type: application/json" \
  -d '{"message":"Explain the 7-capability architecture in 3 bullets"}'
```

---

## Safety Model

Tool execution is **deny-by-default**:

- unknown tool → DENY
- destructive / network tools → APPROVAL required
- read-only registered tools → ALLOW
- provider fallback **never** bypasses policy
- autofix only runs inside explicit policy bounds and records evidence

---

## Related X4 Modules

| Module | Role |
|--------|------|
| [x4-core](https://github.com/dhe-cruzer69/x4-core) | Shared runtime primitives |
| [x4-agents](https://github.com/dhe-cruzer69/x4-agents) | Multi-agent orchestration |
| [x4-mcp](https://github.com/dhe-cruzer69/x4-mcp) | Production MCP gateway |
| [x4-approval](https://github.com/dhe-cruzer69/x4-approval) | Human-in-the-loop gates |
| [x4-evidence](https://github.com/dhe-cruzer69/x4-evidence) | Evidence ledger |
| [x4-router-score](https://github.com/dhe-cruzer69/x4-router-score) | Intelligent routing |
| [x4-sec](https://github.com/dhe-cruzer69/x4-sec) | Security scanner |
| [x4-obs](https://github.com/dhe-cruzer69/x4-obs) | Telemetry & receipts |

---

## Development & Quality Gates

```bash
pytest -q
ruff check .
python -m compileall -q src tests
```

Required gates before any release:

- install • unit tests • integration tests • lint • typecheck  
- secret scan • permissions • documentation • clean-machine start • release build

One unresolved required gate → **UNKNOWN**, not green.

---

## License

Apache-2.0

---

Part of the [X4 / ARIEX4Ops](https://github.com/dhe-cruzer69) portfolio.  
**Profile cleanup in progress** — only high-quality, completed, integrated repos remain.
