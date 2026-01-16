from django.shortcuts import render

# Create your views here.

import joblib
import numpy as np
from django.shortcuts import render

MODEL_PATH = "screening/ml/parki_xgb_model.pkl"

bundle = joblib.load(MODEL_PATH)
scaler = bundle["scaler"]
model = bundle["model"]
features = bundle["features"]

def home(request):
    return render(request, "home.html")

def predict(request):
    if request.method == "POST":
        values = []

        for feature in features:
            value = float(request.POST.get(feature))
            values.append(value)

        data = np.array(values).reshape(1, -1)
        data_scaled = scaler.transform(data)
        prediction = model.predict(data_scaled)[0]

        result = "Parkinson’s Detected" if prediction == 1 else "No Parkinson’s Detected"

        return render(request, "result.html", {
            "result": result,
            "values": zip(features, values)
        })

    return render(request, "predict.html", {"features": features})


