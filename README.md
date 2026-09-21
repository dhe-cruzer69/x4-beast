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

## Architecture

```text
                         ┌─────────────────────┐
                         │       HUMAN         │
                         │ Goal / Approval     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   ORCHESTRATOR      │
                         │ Plan / Delegate     │
                         │ State / Recovery    │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
               ┌─────────┐    ┌─────────┐    ┌─────────┐
               │ Agent A │    │ Agent B │    │ Agent C │
               │ Research│    │ Coding  │    │ Security│
               └────┬────┘    └────┬────┘    └────┬────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    MODEL ROUTER     │
                         │ capability          │
                         │ cost / latency      │
                         │ reliability         │
                         └──────────┬──────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    MCP / TOOLS      │
                         │ GitHub / Files / API│
                         │ DB / Browser / etc. │
                         └──────────┬──────────┘
                                    ▼
                         ┌─────────────────────┐
                         │     SANDBOX         │
                         │ permissions         │
                         │ secrets             │
                         │ policy enforcement  │
                         └──────────┬──────────┘
                                    ▼
                         ┌─────────────────────┐
                         │     VERIFY          │
                         │ tests / inspection  │
                         │ evidence / receipts │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                    VERIFIED                FAILED
                         │                     │
                         ▼                     ▼
                      DONE              RECOVER / RETRY
                                               │
                                               └──→ HUMAN
```

## Key Principle

```
INTENT → PLAN → EXECUTE → OBSERVE → VERIFY → EVIDENCE → SUCCESS

If verification fails:
FAIL → DIAGNOSE → RECOVER → RETRY → VERIFY AGAIN

If confidence cannot be established:
UNKNOWN → HUMAN REVIEW REQUIRED
```

## Features (v0.1.0)

- Multiple model providers: Ollama, OpenAI, OpenRouter, Groq, Mistral, NVIDIA NIM, Gemini
- Capability-aware model routing and fallback
- MCP tool connectors (config-first)
- Explicit tool policy: allow / deny / approval (deny-by-default)
- Audit events with SHA-256 request fingerprints
- FastAPI API + CLI
- Local SQLite / JSONL audit storage
- No secrets stored in source code
- `UNKNOWN` stays `UNKNOWN` until verified

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
cp .env.example .env
python -m x4_beast doctor
python -m x4_beast serve
```

API: `http://127.0.0.1:8787`

## Safety model

Tool execution is **deny-by-default**.

- unknown tool → DENY
- destructive-looking tool → APPROVAL
- network tool → APPROVAL
- explicitly registered read-only tool → ALLOW
- expired/invalid approval → DENY
- provider fallback never bypasses policy

## Evidence states

`OBSERVED` → `CORRELATED` → `HYPOTHESIS` → `VALIDATED` → or `UNKNOWN`

## License

Apache-2.0

---

Part of the [X4 / ARIEX4Ops](https://github.com/dhe-cruzer69) agent infrastructure portfolio.
