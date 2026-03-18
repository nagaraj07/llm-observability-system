# llm-observability-system

This project demonstrates monitoring of LLM applications
using Prometheus and Grafana.

Features
- Prompt latency tracking
- Token usage monitoring
- Request metrics
- Prometheus exporter
- Grafana dashboard

Tech Stack
FastAPI
Prometheus
Grafana
OpenAI

Run

pip install -r requirements.txt
uvicorn app:app --reload
docker-compose up