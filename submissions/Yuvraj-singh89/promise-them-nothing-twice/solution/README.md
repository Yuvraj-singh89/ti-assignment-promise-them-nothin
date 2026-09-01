# RelayAPI

A small distributed per-customer rate limiting prototype.

## Architecture

Multiple stateless application nodes use Redis as shared rate-limit state.

    Node 1 ----\
    Node 2 ----- Redis
    Node 3 ----/

Redis atomic INCR operations ensure that requests handled by different
nodes still consume the same customer quota.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
