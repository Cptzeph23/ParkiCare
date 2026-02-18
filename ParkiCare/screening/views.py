from django.shortcuts import render
import numpy as np
import joblib
from notifications.gava import send_sms

# Load model once (this part is OK at top-level)
model_bundle = joblib.load("screening/ML/parki_xgb_model.pkl")

 # Human-readable explanations for the ML features
feature_guide = {
    "MDVP:Fo(Hz)": ("Fundamental Frequency", "Average vocal frequency", "Normal: 85–255 Hz"),
    "MDVP:Fhi(Hz)": ("Max Frequency", "Highest vocal frequency", "Normal: < 300 Hz"),
    "MDVP:Flo(Hz)": ("Min Frequency", "Lowest vocal frequency", "Normal: > 70 Hz"),
    "MDVP:Jitter(%)": ("Jitter Percent", "Frequency variation in voice", "Normal: < 0.01"),
    "MDVP:Jitter(Abs)": ("Absolute Jitter", "Cycle-to-cycle variation", "Normal: very low"),
    "MDVP:RAP": ("Relative Average Perturbation", "Short-term voice instability", "Normal: < 0.02"),
    "MDVP:PPQ": ("Pitch Perturbation Quotient", "Pitch variation", "Normal: small"),
    "Jitter:DDP": ("Jitter DDP", "Derivative of RAP", "Normal: low"),
    "MDVP:Shimmer": ("Shimmer", "Amplitude variation", "Normal: < 0.03"),
    "MDVP:Shimmer(dB)": ("Shimmer dB", "Amplitude variation (decibels)", "Normal: low"),
    "Shimmer:APQ3": ("Amplitude Perturbation Q3", "Voice amplitude instability", "Normal: low"),
    "Shimmer:APQ5": ("Amplitude Perturbation Q5", "Amplitude variation window", "Normal: low"),
    "MDVP:APQ": ("Amplitude Perturbation Quotient", "Amplitude irregularities", "Normal: low"),
    "Shimmer:DDA": ("DDA", "Average shimmer difference", "Normal: low"),
    "NHR": ("Noise-to-Harmonic Ratio", "Noise in voice signal", "Normal: < 0.02"),
    "HNR": ("Harmonic-to-Noise Ratio", "Voice clarity", "Normal: high (>20)"),
    "RPDE": ("Recurrence Period Density Entropy", "Signal complexity", "Normal: lower"),
    "DFA": ("Detrended Fluctuation Analysis", "Signal self-similarity", "Normal: moderate"),
    "spread1": ("Nonlinear Spread 1", "Frequency variation", "Normal: small"),
    "spread2": ("Nonlinear Spread 2", "Signal dispersion", "Normal: small"),
    "D2": ("Correlation Dimension", "Vocal dynamic complexity", "Normal: stable"),
    "PPE": ("Pitch Period Entropy", "Pitch predictability", "Normal: low"),
}

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
                guide_list = []
                for f in features:
                    g = feature_guide.get(f)
                    if g:
                        guide_list.append((f, g[0], g[1], g[2]))
                return render(request, "predict.html", {
                    "features": features,
                    "guide_list": guide_list,
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

    guide_list = []
    for f in features:
        g = feature_guide.get(f)
        if g:
            guide_list.append((f, g[0], g[1], g[2]))
    return render(request, "predict.html", {
        "features": features,
        "guide_list": guide_list,
    })



    

   
