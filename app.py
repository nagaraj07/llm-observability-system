import os
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama import Client, ResponseError

from prometheus_client import start_http_server
from metrics import REQUEST_COUNT, REQUEST_LATENCY, TOKEN_USAGE

app = FastAPI()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
client = Client(host=OLLAMA_BASE_URL)

start_http_server(8001)

class Prompt(BaseModel):
    prompt: str


@app.post("/generate")
def generate_text(p: Prompt):

    REQUEST_COUNT.inc()

    start = time.time()

    try:
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": p.prompt}],
        )
    except ResponseError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "Unable to reach local Ollama model. Ensure Ollama is running and model is pulled."
            ),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while generating response from Ollama.",
        ) from exc

    latency = time.time() - start
    REQUEST_LATENCY.observe(latency)

    answer = response["message"]["content"]

    tokens = int(response.get("eval_count") or 0)
    TOKEN_USAGE.inc(tokens)

    return {
        "response": answer,
        "latency": latency,
        "tokens": tokens
    }