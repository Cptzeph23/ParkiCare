from django.shortcuts import render
import numpy as np
import joblib
from notifications.gava import send_sms

# Load model once (this part is OK at top-level)
model_bundle = joblib.load("screening/ML/parki_xgb_model.pkl")
model = model_bundle["model"]
scaler = model_bundle["scaler"]
features = model_bundle["features"]


def predict(request):
    if request.method == "POST":
        # 1️⃣ Collect input data
        input_data = []

        for feature in features:
            value = float(request.POST.get(feature))
            input_data.append(value)

        input_array = np.array(input_data).reshape(1, -1)

        # 2️⃣ Scale data
        data_scaled = scaler.transform(input_array)

        # 3️⃣ Make prediction
        prediction = model.predict(data_scaled)[0]
        result = "Parkinson’s Detected" if prediction == 1 else "No Parkinson’s Detected"

        # 🔔 DEBUG LOGS
        print("✅ PREDICTION COMPLETE:", result)
        print("📦 SESSION PHONE:", request.session.get("user_phone"))

        # 4️⃣ Send SMS
        phone = request.session.get("user_phone")
        if phone:
            message = (
                f"ParkiCare Screening Result:\n"
                f"{result}\n"
                f"This is an AI-based preliminary screening."
            )
            send_sms(phone, message)
        else:
            print("❌ NO PHONE NUMBER FOUND — SMS SKIPPED")

        # 5️⃣ Return result
        return render(request, "screening/result.html", {
            "result": result
        })

    # GET request
    return render(request, "screening/predict.html")
