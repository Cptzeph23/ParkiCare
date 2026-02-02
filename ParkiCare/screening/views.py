from django.shortcuts import render
import numpy as np
import joblib
from notifications.gava import send_sms

# Load model once (this part is OK at top-level)
model_bundle = joblib.load("screening/ML/parki_xgb_model.pkl")
model = model_bundle["model"]
scaler = model_bundle["scaler"]
features = model_bundle["features"]

def home(request):
    return render(request, "home.html")

def predict(request):
    if request.method == "POST":
        input_data = []

        for feature in features:
            raw_value = request.POST.get(feature)

            if raw_value is None or raw_value == "":
                return render(request, "predict.html", {
                    "features": features,
                    "error": "Please fill in all fields before submitting."
                })

            input_data.append(float(raw_value))

        input_array = np.array(input_data).reshape(1, -1)
        data_scaled = scaler.transform(input_array)

        prediction = model.predict(data_scaled)[0]
        result = "Parkinson’s Detected" if prediction == 1 else "No Parkinson’s Detected"

        print("✅ PREDICTION RESULT:", result)

        phone = request.session.get("user_phone")
        print("📞 SESSION PHONE:", phone)

        if phone:
            print("🚀 CALLING GAVA SEND_SMS")
            send_sms(
                phone,
                f"ParkiCare Screening Result:\n{result}\nAI-based preliminary screening."
            )
        else:
            print("❌ NO PHONE NUMBER IN SESSION — SMS NOT SENT")

        return render(request, "result.html", {
            "result": result
        })

    return render(request, "predict.html", {
        "features": features
    })
