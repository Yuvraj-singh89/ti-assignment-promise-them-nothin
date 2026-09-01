from datetime import datetime, time, timezone


CUSTOMERS = {
    "customer-a": {
        "rpm": 100
    },
    "customer-b": {
        "rpm": 100
    },
    "northwind": {
        "rpm": 300,
        "batch_override": {
            "start": "02:00",
            "end": "04:00",
            "rpm": 1200
        }
    }
}


def get_customer_limit(customer_id: str) -> int:
    """
    Returns the configured RPM limit.

    Northwind has an explicit temporary commercial policy override
    during 02:00-04:00 UTC.
    """

    policy = CUSTOMERS.get(customer_id)

    if policy is None:
        return 100

    override = policy.get("batch_override")

    if override:
        now = datetime.now(timezone.utc).time()

        start = time.fromisoformat(override["start"])
        end = time.fromisoformat(override["end"])

        if start <= now < end:
            return override["rpm"]

    return policy["rpm"]
