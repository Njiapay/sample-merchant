import requests
import os

import hashlib
import hmac


API_KEY = os.environ["API_KEY"]
RETURN_URL = os.environ.get("RETURN_URL", "https://example.com/payment-complete")
API_URL = os.environ.get("API_URL", "https://api-stg.njiapay.com")


def create_intent(amount: int, currency: str) -> str:
    response = requests.post(
        f"{API_URL}/api/intents",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "amount": amount,
            "currency": currency,
            "reference_id": "Test",
            "purchaser_id": "customer-123",
            "return_url": RETURN_URL,
            "allow_remember_credentials": False,
        },
    )

    data = response.json()
    return data["redirect_url"]


def create_mit_intent(amount: int, currency: str) -> str:
    response = requests.post(
        f"{API_URL}/api/intents",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "amount": amount,
            "currency": currency,
            "reference_id": "subscription_init_" + "customer_123",
            "purchaser_id": "customer_123",
            "return_url": RETURN_URL,
            "allow_remember_credentials": True,
            "request_unscheduled_mit": True,
        },
    )

    data = response.json()
    return data["redirect_url"]


def handle_webhook_event(event: dict) -> None:
    event_type = event.get("type")
    content = event.get("content", {})
    event_status = content.get("status")

    match event_type, event_status:
        case "status_change", "success":
            print(
                f"[webhook] payment {content.get('intent_id')} succeeded, fulfilling order {content.get('reference_id')}"
            )
        case "status_change", "failed":
            print(
                f"[webhook] payment {content.get('intent_id')} failed: {content.get('failure_reason')}"
            )
        case "status_change", _:
            print(f"[webhook] payment {content.get('intent_id')} is {event_status}")
        case "payment_credential", _:
            print(
                f"[webhook] payment credential {content.get('credential_id')} for purchaser {content.get('purchaser_id')} is {event_status}"
            )
        case "refund", _:
            print(
                f"[webhook] refund {content.get('intent_id')} of {content.get('amount')} {content.get('currency')} is {event_status}"
            )
        case "canelation", _:
            print(
                f"[webhook] payment {content.get('intent_id')} of {content.get('amount')} has been cancelled"
            )
        case _:
            print(
                f"[webhook] ignoring unhandled event type/status: {event_type} {event_status}"
            )


def verify_signature(
    raw_body: bytes, signature_header: str, secrets: list[str]
) -> bool:
    received = [s.strip().removeprefix("v0=") for s in signature_header.split(",")]

    for secret in secrets:
        expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
        for sig in received:
            if hmac.compare_digest(sig, expected):
                return True
    return False
