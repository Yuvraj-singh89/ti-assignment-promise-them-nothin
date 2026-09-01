import os

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from app.config import get_customer_limit
from app.limiter import check_rate_limit


app = FastAPI(title="RelayAPI")


@app.get("/api/v1/ping")
def ping(
    x_customer_id: str | None = Header(default=None)
):

    if not x_customer_id:
        raise HTTPException(
            status_code=400,
            detail="X-Customer-Id header is required"
        )

    limit = get_customer_limit(x_customer_id)

    allowed, retry_after, count = check_rate_limit(
        x_customer_id,
        limit
    )

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "customer": x_customer_id
            },
            headers={
                "Retry-After": str(retry_after)
            }
        )

    return {
        "message": "pong",
        "customer": x_customer_id,
        "node": os.getenv("NODE_NAME", "node-local"),
        "limit": limit,
        "request_count": count
    }
