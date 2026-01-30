import base64
import requests
from datetime import datetime

# ✅ SAFARICOM SANDBOX DEFAULTS
CONSUMER_KEY = "JD3uycTwiGwABxBzYhhYhRXUaninvhA7AdL9VJya1rAjP7AE"
CONSUMER_SECRET = "bqvruNGtPBE8ZgkzZicxUs3ZFQeMtQkSybVyu9nuVAQ6LiRIGunsYo16ZFJBlsJi"

SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97ddbfaf1e5..."  # sandbox passkey

CALLBACK_URL = "https://webhook.site/b3cb59ca-7bfe-4c1d-a3c8-06ec83f2e319"  # temporary public URL


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    print("TOKEN RAW RESPONSE:", response.text)

    return response.json()["access_token"]


def stk_push(phone, amount):
    token = get_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        (SHORTCODE + PASSKEY + timestamp).encode()
    ).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "ParkiCare",
        "TransactionDesc": "Parkinson Screening"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)

    print("STK RAW RESPONSE:", response.text)

    return response.text