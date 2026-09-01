import httpx

URL = "http://127.0.0.1:8000/api/v1/ping"


def send_requests(customer_id, number):

    allowed = 0
    rejected = 0

    for _ in range(number):

        response = httpx.get(
            URL,
            headers={
                "X-Customer-Id": customer_id
            }
        )

        if response.status_code == 200:
            allowed += 1

        elif response.status_code == 429:
            rejected += 1

    return allowed, rejected


def print_result(name, allowed, rejected):

    print("\n" + "=" * 45)
    print(name)
    print("=" * 45)
    print("Allowed :", allowed)
    print("Rejected:", rejected)


print("TEST 1: Exact quota")

allowed, rejected = send_requests(
    "test-exact",
    100
)

print_result(
    "Exact Quota",
    allowed,
    rejected
)


print("\nTEST 2: One request over quota")

allowed, rejected = send_requests(
    "test-over",
    101
)

print_result(
    "One Over Quota",
    allowed,
    rejected
)


print("\nTEST 3: Customer isolation")

a_allowed, a_rejected = send_requests(
    "customer-a",
    100
)

b_allowed, b_rejected = send_requests(
    "customer-b",
    100
)

print_result(
    "Customer A",
    a_allowed,
    a_rejected
)

print_result(
    "Customer B",
    b_allowed,
    b_rejected
)
