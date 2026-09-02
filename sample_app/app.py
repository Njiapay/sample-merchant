import json
import os
import requests

from flask import Flask, abort, redirect, render_template, request
from werkzeug.wrappers.response import Response

from .payment import (
    create_intent,
    create_mit_intent,
    handle_webhook_event,
    verify_signature,
)

_API_KEY = os.environ["API_KEY"]
_API_URL = os.environ.get("API_URL", "https://api-stg.njiapay.com")
_WEBHOOK_SECRETS = [s for s in os.environ["WEBHOOK_SECRETS"].split(",") if s]

_CART = {
    "line_items": [
        {"name": "Premium Plan", "quantity": 1, "price": 10.00},
    ],
    "currency": "ZAR",
}

app = Flask(__name__)


@app.get("/")
def landing():
    return render_template("landing.html")


@app.get("/cart/<mode>")
def cart(mode: str):
    if mode not in ("regular", "mit"):
        abort(404)
    total = sum(item["price"] * item["quantity"] for item in _CART["line_items"])
    return render_template("cart.html", cart=_CART, total=total, mode=mode)


@app.post("/checkout/<mode>")
def checkout(mode: str) -> Response:
    total = int(
        sum(item["price"] * item["quantity"] for item in _CART["line_items"]) * 100
    )
    if mode == "regular":
        redirect_url = create_intent(total, _CART["currency"])
    elif mode == "mit":
        redirect_url = create_mit_intent(total, _CART["currency"])
    else:
        abort(404)
    return redirect(redirect_url)


@app.get("/payment-complete")
def payment_complete() -> str:
    intent_id = request.args.get("intent_id", type=str)

    response = requests.get(
        f"{_API_URL}/api/intents/{intent_id}",
        headers={"Authorization": f"Bearer {_API_KEY}"},
    )
    intent = response.json()

    match intent["status"]:
        case "success":
            return render_template("payment_complete.html")
        case "pending":
            return render_template("payment_pending.html")
        case "failed" | "canceled":
            return render_template("payment_failed.html")
        case _:
            raise Exception("Something went wrong")


@app.route("/webhook", methods=["POST"])
def webhook():
    signature_header = request.headers.get("Njiapay-Signature", "")
    if not verify_signature(request.get_data(), signature_header, _WEBHOOK_SECRETS):
        return "Invalid signature", 401
    event = json.loads(request.get_data())

    try:
        handle_webhook_event(event)
        return "OK", 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return "Error", 500


def main() -> None:
    app.run(debug=True)
