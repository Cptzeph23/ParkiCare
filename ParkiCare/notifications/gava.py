import requests
from django.conf import settings

# def send_sms(phone, message):
#     payload = {
#         "apiKey": settings.GAVA_API_KEY,
#         "senderId": settings.GAVA_SENDER_ID,
#         "message": message,
#         "phone": phone
#     }

#     try:
#         response = requests.post(settings.GAVA_API_URL, json=payload, timeout=10)
#         print("GAVA STATUS:", response.status_code)
#         print("GAVA RESPONSE:", response.text)
#         return response.status_code == 200
#     except Exception as e:
#         print("GAVA ERROR:", e)
#         return False

import requests

GAVA_API_KEY = "YOUR_GAVA_API_KEY"
GAVA_SENDER_ID = "ParkiCare"

def send_sms(phone, message):
    url = "https://api.gavaconnect.com/sms/send"  # confirm exact endpoint

    payload = {
        "apiKey": GAVA_API_KEY,
        "senderId": GAVA_SENDER_ID,
        "message": message,
        "phone": phone
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        print("📨 GAVA STATUS CODE:", response.status_code)
        print("📨 GAVA RESPONSE:", response.text)
        return response.json()
    except Exception as e:
        print("❌ GAVA SMS ERROR:", e)
        return None




