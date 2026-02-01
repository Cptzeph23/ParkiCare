import base64
import requests
from datetime import datetime

# ✅ SAFARICOM SANDBOX DEFAULTS
CONSUMER_KEY = "xbN25D14dp01jUR5qr4rdr0BWjme0szyCKwmcQe44XzOjaFn"
CONSUMER_SECRET = "H8wWABpsZH66kjgCCvrTXV6Ue1UPA3TbWLDlwDcE92QdxnGvCQFk8KXNyjCdcYs2"

SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97ddbfaf1e5..."  # sandbox passkey

CALLBACK_URL = "https://webhook.site/your-unique-id"


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        response = requests.get(
            url,
            auth=(CONSUMER_KEY, CONSUMER_SECRET),
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        print("❌ NETWORK ERROR:", e)
        return None

    print("STATUS CODE:", response.status_code)
    print("TOKEN RAW RESPONSE:", response.text)

    if response.status_code != 200:
        return None

    try:
        return response.json().get("access_token")
    except Exception as e:
        print("❌ JSON PARSE ERROR:", e)
        return None



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

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)

    print("STK STATUS:", response.status_code)
    print("STK RESPONSE:", response.text)

    try:
        return response.json()
    except:
        return None
