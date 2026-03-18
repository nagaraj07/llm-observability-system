from prometheus_client import Counter, Histogram

# total requests
REQUEST_COUNT = Counter(
    "llm_requests_total",
    "Total LLM requests"
)

# latency
REQUEST_LATENCY = Histogram(
    "llm_request_latency_seconds",
    "Latency of LLM requests"
)

# token usage
TOKEN_USAGE = Counter(
    "llm_tokens_used_total",
    "Total tokens used"
)

# hallucination metric
HALLUCINATION_COUNT = Counter(
    "llm_hallucination_total",
    "Detected hallucinations"
)