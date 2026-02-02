import base64
import requests
from datetime import datetime

CONSUMER_KEY = "xbN25D14dp01jUR5qr4rdr0BWjme0szyCKwmcQe44XzOjaFn"
CONSUMER_SECRET = "H8wWABpsZH66kjgCCvrTXV6Ue1UPA3TbWLDlwDcE92QdxnGvCQFk8KXNyjCdcYs2"

SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97ddbfaf1e5a"

CALLBACK_URL = "https://webhook.site/cf9630eb-85df-4dd0-8085-7cd9a5aa834c"


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    print("TOKEN:", response.text)
    return response.json().get("access_token")


def stk_push(phone, amount):
    token = get_access_token()
    if not token:
        return None

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
        "TransactionDesc": "Parkinson Screening Payment"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    print("STK RESPONSE:", response.text)
    return response.json()
