from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import logging
from prometheus_client import Gauge, Counter, generate_latest
import time

logger = logging.getLogger(__name__)

start_time = time.time()
uptime = Gauge('app_uptime_seconds', 'Application uptime')
uptime.set(start_time)

request_count = Counter('app_requests_total', 'Total requests')

app = FastAPI()

class ProcessRequest(BaseModel):
    content: str

@app.post("/process")
async def process_request(request: ProcessRequest):
    """Process incoming API request with LLM."""
    try:
        request_count.inc()
        # Placeholder for LLM processing
        response = f"Processed: {request.content}"
        logger.info(f"API request processed: {request.content}")
        return {"response": response}
    except Exception as e:
        logger.error(f"API processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")