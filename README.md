# X4 BEAST System

**Local-first, provider-agnostic AI agent infrastructure** implementing the 7-capability autonomous agent architecture.

> The system should never equate execution with success.

## The 7 Capabilities

| # | Capability | Core mechanism | Success criterion |
|---|---|---|---|
| 1 | Reliable autonomous execution | Planner + executor + retry/recovery loop | Goal completed across multiple tools |
| 2 | Verification before success | Tests + output inspection + evidence ledger | No PASS without evidence |
| 3 | Secure tools & credentials | Sandbox + least privilege + secret isolation + policy gates | Unsafe actions blocked |
| 4 | Persistent context & memory | State store + project memory + task history | Agent resumes work correctly |
| 5 | Multi-agent orchestration | Delegation + specialist agents + coordinator | Complex tasks decomposed effectively |
| 6 | Intelligent routing | Capability/cost/latency/reliability router | Best available model/tool selected dynamically |
| 7 | Human-in-the-loop control | Approval gates + uncertainty states + escalation | High-impact actions require human approval |

## Quick Start (Manual)

```bash
git clone https://github.com/dhe-cruzer69/x4-beast.git
cd x4-beast

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
cp .env.example .env
# Edit .env and add only the keys you actually use

python -m x4_beast doctor          # Check providers
python -m x4_beast serve           # Start API on http://127.0.0.1:8787
```

---

## Automatic Setup (Recommended)

### Option 1 — One-command start script (simplest)

```bash
# Make the script executable
chmod +x scripts/start.sh

# Run it (starts in background and logs to data/x4-beast.log)
./scripts/start.sh

# Stop later
./scripts/stop.sh
```

### Option 2 — Docker (fully automatic + isolated)

```bash
# Build and start (detached)
docker compose up -d --build

# View logs
docker compose logs -f

# Stop
docker compose down
```

The container restarts automatically on reboot (`restart: unless-stopped`).

### Option 3 — systemd service (Linux — starts on boot)

```bash
# 1. Install the service file
sudo cp deploy/x4-beast.service /etc/systemd/system/

# 2. Edit paths if needed (default assumes /opt/x4-beast)
sudo nano /etc/systemd/system/x4-beast.service

# 3. Enable + start
sudo systemctl daemon-reload
sudo systemctl enable --now x4-beast

# Check status
sudo systemctl status x4-beast
journalctl -u x4-beast -f
```

---

## Environment Variables

Copy `.env.example` → `.env` and fill only what you need:

```env
X4_HOST=127.0.0.1
X4_PORT=8787

# Local (preferred)
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b

# Cloud (optional)
OPENAI_API_KEY=
OPENROUTER_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
NVIDIA_API_KEY=
GEMINI_API_KEY=
```

The router always tries **Ollama first**. Cloud providers are used only as fallback.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health + available providers |
| POST | `/v1/chat` | Simple chat |
| POST | `/v1/agent/run` | Full agent loop with tools + policy |

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

---

## Development

```bash
pytest -q
ruff check .
python -m compileall -q src tests
```

No command converts a failed check into PASS.

## License

Apache-2.0

---

Part of the [X4 / ARIEX4Ops](https://github.com/dhe-cruzer69) portfolio.
