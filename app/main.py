from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Order Service",
    version="1.0.0",
)


class OrderRequest(BaseModel):
    customer_id: str
    product_id: str
    quantity: int


orders = {}


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/ready")
def readiness():
    return {
        "status": "ready"
    }


@app.post("/orders", status_code=201)
def create_order(order: OrderRequest):
    order_id = str(uuid4())

    orders[order_id] = {
        "order_id": order_id,
        "customer_id": order.customer_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "created",
    }

    return orders[order_id]


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = orders.get(order_id)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order