# llm-observability-system

This is a simple, hands-on project to understand LLM observability.
It uses a local Ollama model with a FastAPI app, then tracks usage and performance in Prometheus and Grafana.

## What This Project Does

- Serves a `POST /generate` endpoint for LLM responses.
- Uses a local Ollama model (default: `llama3.2:latest`).
- Exposes Prometheus metrics on port `8001`.
- Visualizes metrics with Prometheus and Grafana via Docker Compose.

## Tech Stack

- FastAPI
- Ollama (local LLM runtime)
- Prometheus
- Grafana
- Prometheus Python client

## Project Structure

- `app.py`: FastAPI app, local LLM call, and metric updates.
- `metrics.py`: metric definitions (request count, latency, tokens).
- `prometheus.yml`: tells Prometheus where to scrape metrics.
- `docker-compose.yml`: runs Prometheus and Grafana.
- `requirements.txt`: Python packages needed by the app.

## Prerequisites

- Python 3.x
- Ollama installed and running
- Docker / Rancher Desktop for Prometheus + Grafana

## Setup

1. Create and activate virtual environment:

```bash
python3 -m venv env3
source env3/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Start Ollama and pull the default model:

```bash
ollama serve
ollama pull llama3.2:latest
```

If `llama3.2:latest` is already downloaded, you can skip the pull command.

4. Start monitoring stack:

```bash
docker-compose up -d
```

5. Start FastAPI app:

```bash
uvicorn app:app --reload
```

## Environment Variables

- `OLLAMA_BASE_URL` default: `http://localhost:11434`
- `OLLAMA_MODEL` default: `llama3.2:latest`

Example:

```bash
export OLLAMA_MODEL=llama3.2:latest
export OLLAMA_BASE_URL=http://localhost:11434
```

## API Usage

Endpoint:

- `POST /generate`

The API takes a prompt and returns the model response, request latency, and token count.

Request:

```json
{
	"prompt": "Explain observability in two lines"
}
```

Sample curl:

```bash
curl -X POST http://127.0.0.1:8000/generate \
	-H "Content-Type: application/json" \
	-d '{"prompt":"Explain observability in two lines"}'
```

Response:

```json
{
	"response": "...",
	"latency": 0.42,
	"tokens": 28
}
```

## Metrics Exposed

From `metrics.py`:

- `llm_requests_total`
- `llm_request_latency_seconds`
- `llm_tokens_used_total`
- `llm_hallucination_total` (defined but not incremented in app yet)

Metrics endpoint:

- `http://127.0.0.1:8001/metrics`

You can open this URL directly to confirm metrics are being published.

## Monitoring UI

- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3000`
- Default Grafana login: `admin / admin`

## Test Checklist

1. `docker-compose ps` shows Prometheus and Grafana running.
2. `curl http://127.0.0.1:8001/metrics` returns metrics text.
3. `POST /generate` returns JSON with `response`, `latency`, and `tokens`.
4. Prometheus query `llm_requests_total` increases after requests.

## Common Issues

- `502` from `/generate`: Ollama not running or model not pulled.
  - Fix: run `ollama serve` and `ollama pull llama3.2:latest`.
- Docker image pull timeout in corporate network:
  - Configure proxy for Rancher Desktop/Docker daemon.
- `externally-managed-environment` on pip:
  - Use a local virtual environment and `python -m pip`.