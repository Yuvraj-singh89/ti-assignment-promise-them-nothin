

## Conflict resolution

The CTO requires that customers never exceed their contracted quota, while
Support requires Northwind to avoid HTTP 429 during a 02:00-04:00 UTC batch
window even though its contracted quota is 300 RPM and its traffic can reach
800-1200 RPM.

These requirements cannot both literally be true if the Northwind quota
remains fixed at 300 RPM.

I rejected a hidden customer-specific bypass. Instead, Northwind's exception
is represented as an explicit configuration-based policy override with a
bounded UTC time window. During the configured batch window, the approved
limit is 1200 RPM.

This makes the exception visible and auditable rather than hiding business
logic inside the rate limiter.

## Technical design

The implementation uses a Redis-backed fixed-window counter.

Each customer receives a key containing the customer ID and current
60-second window.

Redis INCR is atomic. Therefore, multiple stateless application nodes sharing
the same Redis instance enforce one global customer quota.

The first request sets a TTL so counters expire automatically.

A fixed window is intentionally simple and easy to audit. Its limitation is
that bursts can occur near window boundaries.

## Verification

The harness verifies:

- Exactly quota requests are accepted.
- Requests above quota receive HTTP 429.
- Different customers have independent quotas.

The shared Redis design also means multiple application nodes use the same
counter.

This prototype does not prove production-scale Redis availability, failover,
network partition handling, or protection against boundary bursts.

## If I had four more hours

I would add:

1. Docker Compose with three application nodes and a load balancer.
2. Concurrent load tests across all nodes.
3. Metrics and structured audit logging.
4. Redis failure and recovery testing.
5. More robust sliding-window rate limiting.
