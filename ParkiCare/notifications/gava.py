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

def send_sms(phone, message):
    print(f"DEMO SMS to {phone}: {message}")
    return True



