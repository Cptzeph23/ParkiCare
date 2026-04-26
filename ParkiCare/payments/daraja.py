import base64
from datetime import datetime

import certifi
import requests
from django.conf import settings


def _cfg(name, default=""):
    return str(getattr(settings, name, default)).strip()


def _host():
    return "api.safaricom.co.ke" if getattr(settings, "DARAJA_LIVE_STK", False) else "sandbox.safaricom.co.ke"


def _normalize_phone(phone):
    raw = str(phone or "").strip().replace(" ", "")
    if raw.startswith("+"):
        raw = raw[1:]
    if raw.startswith("0"):
        raw = "254" + raw[1:]
    if raw.startswith("7") and len(raw) == 9:
        raw = "254" + raw

    if not raw.isdigit() or len(raw) != 12 or not raw.startswith("254"):
        return None
    return raw


def _sandbox_test_numbers():
    numbers = getattr(settings, "DARAJA_SANDBOX_ALLOWED_MSISDNS", ["254708374149"])
    return {str(item).strip() for item in numbers if str(item).strip()}


def get_access_token():
    consumer_key = _cfg("DARAJA_CONSUMER_KEY", "xbN25D14dp01jUR5qr4rdr0BWjme0szyCKwmcQe44XzOjaFn")
    consumer_secret = _cfg("DARAJA_CONSUMER_SECRET", "H8wWABpsZH66kjgCCvrTXV6Ue1UPA3TbWLDlwDcE92QdxnGvCQFk8KXNyjCdcYs2")
    if not consumer_key or not consumer_secret:
        return None

    url = f"https://{_host()}/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(
            url,
            auth=(consumer_key, consumer_secret),
            timeout=10,
            verify=certifi.where(),
        )
        body = response.json()
        return body.get("access_token")
    except Exception as e:
        print("ACCESS TOKEN EXCEPTION:", e)
        return None


def stk_push(phone, amount, account_reference="ParkiCare", transaction_desc="Parkinson Screening Payment"):
    shortcode = _cfg("DARAJA_SHORTCODE", "174379")
    passkey = _cfg("DARAJA_PASSKEY", "bfb279f9aa9bdbcf158e97ddbfaf1e5a")
    callback_url = _cfg("DARAJA_CALLBACK_URL", "https://webhook.site/cf9630eb-85df-4dd0-8085-7cd9a5aa834c")
    normalized_phone = _normalize_phone(phone)
    is_live = getattr(settings, "DARAJA_LIVE_STK", False)

    if not normalized_phone:
        return {"errorCode": "INVALID_PHONE", "errorMessage": "Use phone format 2547XXXXXXXX."}
    if not shortcode or not passkey or not callback_url:
        return {"errorCode": "CONFIG_ERROR", "errorMessage": "Daraja shortcode/passkey/callback is missing."}
    if is_live and shortcode == "174379":
        return {
            "errorCode": "LIVE_CONFIG_MISMATCH",
            "errorMessage": "Live STK is enabled but sandbox shortcode (174379) is configured.",
        }

    if not is_live and normalized_phone not in _sandbox_test_numbers():
        return {
            "errorCode": "SANDBOX_MSISDN_NOT_ALLOWED",
            "errorMessage": "Sandbox STK only works on approved test MSISDNs. Switch to live credentials for real phones.",
        }

    token = get_access_token()
    if not token:
        return {"errorCode": "TOKEN_FAIL", "errorMessage": "Could not generate access token."}

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": normalized_phone,
        "PartyB": shortcode,
        "PhoneNumber": normalized_phone,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    endpoint = f"https://{_host()}/mpesa/stkpush/v1/processrequest"

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=10,
            verify=certifi.where(),
        )
        body = response.json()
        print("STK ENDPOINT:", endpoint)
        print("STK RESPONSE:", body)
        return body
    except Exception as e:
        print("STK PUSH EXCEPTION:", e)
        return {"errorCode": "EXCEPTION", "errorMessage": str(e)}


def demo_stk_push(phone=None, amount=50):
    return stk_push(
        phone=phone or "254708374149",
        amount=amount,
        account_reference="ParkiCare DEMO",
        transaction_desc="Sandbox Demo STK Push",
    )
