# MetricMind 🧠

An agentic, semantic BI engine that lets you ask business questions in plain English — and get back **governed, trustworthy answers**, never hallucinated SQL.

## The Problem

Giving an AI direct access to a data warehouse for "Text-to-SQL" is risky: the AI can hallucinate joins, ignore business logic, and produce numbers that don't match official reports. MetricMind solves this by making the AI talk **only** to a governed semantic layer — never raw tables.

## Architecture

User → Next.js Chat UI → FastAPI + LangChain Agent → dbt Semantic Layer (MetricFlow) → Snowflake

- **Data Warehouse:** Snowflake, holding 5,000+ transaction records
- **Transformation:** dbt models (`stg_transactions` → `fct_sales`) with automated data quality tests
- **Semantic Layer:** dbt + MetricFlow, defining `revenue`, `cost`, and `margin` as governed metrics with one exact formula, used everywhere
- **Agentic Orchestrator:** LangChain + local Llama 3.2 (via Ollama), routing questions to either a simple metric lookup or a full multi-step root-cause investigation
- **API:** FastAPI backend exposing a single `/chat` endpoint
- **Frontend:** Next.js + Tailwind chat interface, with a "View API Call" transparency feature showing the exact governed query used for every answer

## Key Features

- **Governance audit-proven:** the same question always returns the exact same number — verified by running identical queries repeatedly
- **Root-cause investigation:** ask "why did margins drop?" and MetricMind automatically finds the worst-performing quarter, drills into the cost breakdown by product, and explains the cause with real numbers
- **Cost governance:** every query is logged with a timestamp, and a session query limit prevents runaway costs
- **Full transparency:** every answer includes a "View API Call" link showing the exact semantic layer command used — no black-box AI

## Tech Stack

| Layer          | Technology                     |
|----------------|--------------------------------|
| Data Warehouse | Snowflake                      |
| Transformation | dbt Core                       |
| Semantic Layer | dbt + MetricFlow               |
| AI Agent       | LangChain + Ollama (Llama 3.2) |
| Backend API    | FastAPI                        |
| Frontend       | Next.js, Tailwind CSS, Tremor  |

## Running Locally

1. Set up Snowflake and load transaction data (see `warehouse/generate_data.py`)
2. Run `dbt run` in `warehouse/metricmind_dbt` to build models
3. Start the agent API: `cd agent && uvicorn main:app --reload`
4. Start the frontend: `cd frontend && npm run dev`
5. Visit `http://localhost:3000`

## Example Questions

- "What is our revenue by region?"
- "What is our cost by product?"
- "Why did our margins drop?"

---

Built as a hands-on exploration of agentic BI and semantic layer governance.