# NetSage AI — AI-Assisted Network Troubleshooting with Human Review

NetSage AI is a standalone academic prototype for analysing Cisco Packet Tracer-style lab evidence. A user submits a symptom, topology notes and show-command output. The system runs deterministic checks, creates an evidence-grounded recommendation, and requires a person to accept, edit, or reject it. It never changes a device configuration.

## Features and architecture

React/Vite provides the dashboard, workspace and review history. FastAPI/Pydantic provides a typed REST API, SQLite persists cases, diagnoses, reviews, rule findings and verification records, and Python rules provide auditable non-LLM checks. The included 31 cases are clearly authored lab/demo scenarios; they are not represented as Packet Tracer-verified runs.

Workflow: **Case → evidence → rule checker → AI diagnosis → human review → suggested fix → verification**. The current default is explicitly labelled `DEMO_FALLBACK`: deterministic, authored logic used when no AI provider is configured. It is not a real LLM response. `prompts/diagnose_prompt.md` provides the provider-ready evidence-grounding prompt.

Implemented checks: duplicate IP, subnet-mask conflict, gateway mismatch, administratively down interface, missing VLAN, missing route, and trunk issue. Findings only report PASS where supplied text supports it; otherwise they say `INSUFFICIENT_EVIDENCE`.

The dashboard agreement rate is calculated, not hard-coded: `Accepted AI diagnoses / total reviewed diagnoses`.

## API

- `GET /api/cases`, `GET /api/cases/{case_id}`
- `POST /api/diagnose`, `POST /api/rules/check`
- `POST /api/reviews`, `GET /api/reviews`
- `GET /api/dashboard/stats`, `POST /api/verification`

`POST /api/verification` rejects an unreviewed diagnosis. A review may be `ACCEPTED`, `EDITED` (with a full corrected diagnosis), or `REJECTED`.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Run tests with `python -m pytest`.

## Docker

```powershell
docker compose up --build
```

The frontend is at port 5173 and backend API at port 8000. The compose volume persists the SQLite `data` directory; for a production deployment, mount the database file explicitly and configure CORS/API URL appropriately.

## Limitations

Rule parsing intentionally demonstrates common lab patterns rather than parsing every IOS format. The default AI output is a transparent fallback. To enable a real OpenAI-compatible provider, set `LLM_API_KEY`, `LLM_BASE_URL` (the `/v1` base URL), and `LLM_MODEL`; provider errors safely return a clearly labelled fallback. Human review remains mandatory in all modes.
