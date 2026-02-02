import requests

GAVA_DEMO_MODE = True  
def send_sms(phone, message):
    """
    Demo SMS sender for ParkiCare project.
    Real Gava Connect credentials required for live SMS.
    """
    if GAVA_DEMO_MODE:
        print("📨 [GAVA DEMO SMS]")
        print("📞 PHONE:", phone)
        print("💬 MESSAGE:", message)
        print("✅ SMS FLOW CONFIRMED (NO REAL SMS SENT)")
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
