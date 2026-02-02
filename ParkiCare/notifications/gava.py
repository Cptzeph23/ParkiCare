import requests

GAVA_DEMO_MODE = True  
def send_sms(phone, message):
    if GAVA_DEMO_MODE:
        print("📨 [DEMO SMS]")
        print("📞 TO:", phone)
        print("💬 MESSAGE:", message)
        print("✅ SMS MARKED AS SENT (DEMO MODE)")
        return {
            "status": "demo",
            "phone": phone,
            "message": message
        }

    # REAL MODE (kept for future)
    url = "https://REAL_GAVA_ENDPOINT_HERE"
    payload = {
        "phone": phone,
        "message": message
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        print("📨 GAVA STATUS:", response.status_code)
        print("📨 GAVA RESPONSE:", response.text)
        return response.json()
    except Exception as e:
        print("❌ GAVA SMS ERROR:", e)
        return None
