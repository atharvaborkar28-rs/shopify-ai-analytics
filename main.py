from fastapi import FastAPI
from pydantic import BaseModel
import requests
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI()

SHOPIFY_TOKEN = "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"
API_VERSION = "2024-01"

class QuestionRequest(BaseModel):
    store: str
    question: str


@app.post("/ask")
def ask_question(req: QuestionRequest):
    store = req.store
    question = req.question.lower()

    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Accept": "application/json"
    }

    # ---------------- FETCH ORDERS ----------------
    orders_url = f"https://{store}.myshopify.com/admin/api/{API_VERSION}/orders.json?status=any"
    orders = requests.get(orders_url, headers=headers).json().get("orders", [])

    # ---------------- LAST 30 DAYS ----------------
    now = datetime.utcnow()
    last_30_days = now - timedelta(days=30)

    recent_orders = []
    for o in orders:
        created_at = datetime.strptime(o["created_at"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        if created_at >= last_30_days:
            recent_orders.append(o)

    # ---------------- REVENUE ----------------
    total_revenue = sum(float(o.get("total_price", 0)) for o in recent_orders)

    # ---------------- TOP PRODUCT ----------------
    product_sales = defaultdict(int)
    for o in recent_orders:
        for item in o.get("line_items", []):
            product_sales[item["name"]] += item.get("quantity", 0)

    top_product = max(product_sales, key=product_sales.get) if product_sales else None

    # ---------------- LOYAL CUSTOMERS ----------------
    customer_count = defaultdict(int)
    customer_names = {}

    for o in orders:
        c = o.get("customer")
        if not c:
            continue
        cid = c["id"]
        name = f"{c.get('first_name','')} {c.get('last_name','')}".strip()
        customer_names[cid] = name if name else f"Customer ID {cid}"
        customer_count[cid] += 1

    loyal_customers = [
        f"{customer_names[cid]} – {count} orders"
        for cid, count in customer_count.items()
        if count > 1
    ]

    # ================= QUESTION HANDLING =================

    # ORDERS COUNT
    if "how many orders" in question:
        return {
            "intent": "sales",
            "answer": f"There are {len(orders)} total orders in your store."
        }

    # LAST 30 DAYS ORDERS
    if "last 30 days" in question or "past 30 days" in question:
        return {
            "intent": "sales",
            "answer": f"There are {len(recent_orders)} orders in the last 30 days."
        }

    # REVENUE
    if "revenue" in question or "total sales" in question or "total revenue" in question:
        return {
            "intent": "sales",
            "answer": f"Total revenue in the last 30 days is ₹{total_revenue:.2f}."
        }

    # TOP PRODUCT
    if "most" in question or "top product" in question or "sold the most" in question:
        return {
            "intent": "sales",
            "answer": (
                f"The top selling product in the last 30 days is '{top_product}'."
                if top_product else "No sales data available."
            )
        }

    # LOYAL CUSTOMERS
    if "loyal" in question or "more than once" in question or "repeat" in question:
        return {
            "intent": "customers",
            "answer": loyal_customers if loyal_customers else "No repeat customers found."
        }

    # FALLBACK
    return {
        "intent": "unknown",
        "answer": "Sorry, I could not understand the question."
    }
