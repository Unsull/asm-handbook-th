"""Synthetic object-level authorization function used in educational tests."""

ORDERS = {"order-1": {"owner": "alice", "total": 300}, "order-2": {"owner": "bob", "total": 950}}


def read_order(user_id: str, order_id: str):
    """Return a synthetic order only for its owner; no real authentication here."""
    order = ORDERS.get(order_id)
    if order is None:
        raise KeyError("order not found")
    if order["owner"] != user_id:
        raise PermissionError("forbidden")
    return dict(order)
