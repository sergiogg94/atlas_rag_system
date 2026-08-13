# Atlas RAG System — Agent Guide

This is a personal learning project focused on building a production-ready
Retrieval-Augmented Generation (RAG) system from scratch.
The goal is to deeply understand the entire technology stack required
for modern AI applications.

## Quick start

```bash
cp .env.example .env          # then edit with real API keys
docker compose up --build      # starts db + backend + frontend + dashboard
```

Run without Docker:

```bash
uv sync --group dev --all-extras
# start PostgreSQL 16 + pgvector (e.g. docker run ankane/pgvector)
python -m app.db.init_db
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
python -m app.frontend.app     # Gradio UI
streamlit run app/evaluator/dashboard.py
```

## Commands

| Action | Command |
|---|---|
| Install deps | `uv sync` (add `--group dev --all-extras` for pytest + all services) |
| Regenerate lock | `uv lock` |
| Lock → requirements-backend.txt | `uv pip compile pyproject.toml --extra backend -o requirements-backend.txt` |
| Lock → requirements-frontend.txt | `uv pip compile pyproject.toml --extra frontend -o requirements-frontend.txt` |
| Lock → requirements-dashboard.txt | `uv pip compile pyproject.toml --extra dashboard -o requirements-dashboard.txt` |
| Run all tests | `pytest` (only `tests/test_chunker.py` exists) |
| Single test | `pytest tests/test_chunker.py::test_chunk_text_basic -v` |

No `ruff.toml`, `pytest.ini`, or `mypy.ini` exist — tools run with defaults.

## Architecture

Single Python package under `app/` (not a monorepo). Three services sharing the same codebase:

- **FastAPI backend** (`app/main.py`) — port 8000, 5 endpoints (`/health`, `/ingest`, `/upload`, `/query`, `/search`)
- **Gradio frontend** (`app/frontend/app.py`) — port 7860
- **Streamlit dashboard** (`app/evaluator/dashboard.py`) — port 8501

## Key paths

| Path | Role |
|---|---|
| `app/api/routes.py` | All API endpoints |
| `app/services/rag_service.py` | RAG orchestrator |
| `app/db/models.py` | SQLAlchemy models (Document, Chunk with pgvector) |
| `app/db/init_db.py` | Create pgvector extension and tables |
| `app/core/config.py` | Env-based settings (auto-loads `.env` at import) |
| `app/evaluator/evaluator.py` | RAGEvaluator (retrieval + generation metrics) |
| `test_data/sprint_step/` | 14 test documents |
| `app/evaluator/data/test_dataset_sprintstep_mini.json` | 19 Q&A pairs (AI-generated, not human-reviewed) |
| `scripts/ops/run_evaluation.py` | CLI entrypoint for evaluation runs |

## Gotchas

- **`uv.lock` vs per-service `requirements-*.txt`** can drift. Each Dockerfile installs only its own compiled file (`requirements-backend.txt`, `requirements-frontend.txt`, `requirements-dashboard.txt`). Run `bash scripts/ops/generate_requirements.sh` after changing deps.
- **`torch` is pinned to the CPU-only build** (`torch==X.Y.Z+cpu` via the `pytorch-cpu` index in `pyproject.toml`). `Dockerfile.backend` needs `--extra-index-url https://download.pytorch.org/whl/cpu` to fetch that wheel. No GPU inference.
- **`sys.path.insert(0, ...)`** at `app/evaluator/dashboard.py:9` — fragile path hack.
- **Gradio handlers use `asyncio.run()`** in sync wrappers — can cause nested event loop errors.
- **No CI/CD** — no GitHub Actions workflows. Deployment is via Render (see `render.yaml`).
- **Test dataset** is AI-generated without human review — interpret evaluation results with caution.
- **No async tests** — all service code is async, but no tests use `pytest-asyncio`.
