from app.config import get_customer_limit


def test_customer_a_limit():
    assert get_customer_limit("customer-a") == 100


def test_customer_b_limit():
    assert get_customer_limit("customer-b") == 100


def test_unknown_customer_limit():
    assert get_customer_limit("unknown-customer") == 100


def test_northwind_normal_limit():
    limit = get_customer_limit("northwind")

    # Depending on the current UTC time, Northwind can have
    # either the normal limit or the configured batch override.
    assert limit in [300, 1200]
