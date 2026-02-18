# ParkiCare — Parkinson’s Screening Web App

ParkiCare is a Django-based application that provides an AI-assisted, preliminary screening experience for Parkinson’s disease using voice-derived features. It includes a simple payment step using M-Pesa STK Push (demo flow), a result page, and optional SMS notifications.

## Highlights
- Healthcare-themed, accessible UI with consistent styling
- Predict page with clear feature explanations and typical non-diagnostic ranges
- Demo STK Push to trigger a phone prompt and proceed without payment verification
- Optional SMS notification via GavaConnect

## Technology Stack
- Python 3.12, Django 6
- XGBoost model bundle for inference
- Bootstrap + custom CSS
- Requests + certifi for secure HTTPS calls

## Project Structure
```
ParkiCare/
├── ParkiCare/
│   ├── ParkiCare/
│   │   ├── settings.py               # Django settings (STATICFILES_DIRS, DARAJA_LIVE_STK, etc.)
│   │   ├── urls.py                   # Root URLconf
│   │   ├── wsgi.py / asgi.py         # App servers
│   │   └── __init__.py
│   ├── payments/
│   │   ├── daraja.py                 # Daraja STK Push (sandbox/live toggle, demo_stk_push)
│   │   ├── views.py                  # Pay view → demo STK then redirect to predict
│   │   ├── urls.py                   # /payments/pay/
│   │   └── models.py                 # Payment model (minimal/placeholder)
│   ├── screening/
│   │   ├── views.py                  # Feature guide + prediction flow
│   │   ├── models.py
│   │   └── ML/
│   │       ├── parki_xgb_model.pkl   # Model bundle: { model, scaler, features }
│   ├── notifications/
│   │   ├── gava.py                   # Optional SMS via GavaConnect
│   │   └── models.py
│   ├── templates/
│   │   ├── base.html                 # Global layout and Bootstrap/CSS includes
│   │   ├── home.html                 # Landing page
│   │   ├── pay.html                  # Payment form
│   │   ├── pay_wait.html             # Payment info page
│   │   ├── predict.html              # Screening form + explanation section
│   │   └── result.html               # Prediction result and entered values
│   ├── static/
│   │   └── css/
│   │       └── style.css             # Healthcare theme CSS (hc-* utility classes)
│   └── manage.py
├── README.md                         # This guide
└── requirements.txt                  # Python dependencies
```

## Setup
1. Create and activate a virtual environment
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
2. Install dependencies
   ```bash
   pip install -r ParkiCare/requirements.txt
   ```
3. Run database migrations
   ```bash
   cd ParkiCare
   python manage.py migrate
   ```
4. Start the development server
   ```bash
   python manage.py runserver
   # Open http://127.0.0.1:8000/
   ```

## Configuration
- Static files: ensure STATICFILES_DIRS is set to include the `static` folder in settings
  - See [settings.py](file:///c:/programs/ParkiCare/ParkiCare/ParkiCare/settings.py#L110-L114)
- Daraja STK toggle:
  - `DARAJA_LIVE_STK = True` to use `api.safaricom.co.ke` (expects live credentials)
  - `DARAJA_LIVE_STK = False` to use `sandbox.safaricom.co.ke`
  - See [settings.py](file:///c:/programs/ParkiCare/ParkiCare/ParkiCare/settings.py#L112-L114) and [daraja.py](file:///c:/programs/ParkiCare/ParkiCare/payments/daraja.py#L1-L30)
- Credentials:
  - In [daraja.py](file:///c:/programs/ParkiCare/ParkiCare/payments/daraja.py#L6-L13), set `CONSUMER_KEY`, `CONSUMER_SECRET`, `SHORTCODE`, and `PASSKEY` appropriately.
  - Avoid checking secrets into source control for production.

## Using the App
- Home → click Start Screening to go to Payment
- Payment → enter phone and click Pay
  - The app calls `demo_stk_push` to issue an STK request (live or sandbox based on settings) and then immediately proceeds to Predict without verifying payment
  - See [views.py](file:///c:/programs/ParkiCare/ParkiCare/payments/views.py#L11-L29)
- Predict → fill features and Submit to get AI-assisted result
  - The Explanation/Guide section shows feature meanings and indicative ranges
- Result → shows prediction and the values you entered

## Notes
- The feature guide provides orientation only and is not diagnostic.
- The demo STK flow is intended to show the phone prompt without enforcing payment confirmation.
- For production, move all keys/secrets to environment variables and add proper callback handling.

## Troubleshooting
- CA bundle errors: system-level overrides (REQUESTS_CA_BUNDLE/CURL_CA_BUNDLE) can break TLS. The app forces `verify=certifi.where()` in requests to avoid invalid paths.
- Static assets not loading: verify `STATICFILES_DIRS` and run `python manage.py collectstatic` for production deployments.
