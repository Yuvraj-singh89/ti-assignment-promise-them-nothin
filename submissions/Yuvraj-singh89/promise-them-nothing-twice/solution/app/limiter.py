import time
import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379

client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def check_rate_limit(customer_id: str, limit: int):
    """
    Fixed-window distributed rate limiter.

    Redis INCR is atomic, so multiple application nodes using the
    same Redis instance share one global counter.
    """

    current_time = int(time.time())

    # 60-second fixed window
    window = current_time // 60
    key = f"rate_limit:{customer_id}:{window}"

    count = client.incr(key)

    # First request creates the key, so give it an expiry.
    if count == 1:
        client.expire(key, 60)

    allowed = count <= limit

    # Seconds until the next minute boundary
    retry_after = 60 - (current_time % 60)

    return allowed, retry_after, count
