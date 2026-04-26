from django.conf import settings
from django.shortcuts import redirect, render

from .daraja import demo_stk_push, stk_push
from .models import Payment

def pay(request):
    if request.method == "POST":
        phone = (request.POST.get("phone") or "").strip()
        amount = 50
        use_demo = getattr(settings, "DEMO_PAYMENT_MODE", False)

        response = demo_stk_push(phone, amount) if use_demo else stk_push(phone, amount)

        if response and response.get("ResponseCode") == "0":
            Payment.objects.create(
                phone=phone,
                amount=amount,
                receipt=response.get("CheckoutRequestID", ""),
                status="INITIATED",
            )
            request.session["payment_verified"] = True
            request.session["user_phone"] = phone
            return redirect("/predict/")

        Payment.objects.create(
            phone=phone,
            amount=amount,
            status="FAILED",
        )
        error_message = (
            response.get("errorMessage")
            or response.get("ResponseDescription")
            or response.get("errorCode")
            or "STK push failed. Confirm your number and Daraja credentials."
        )
        return render(request, "pay.html", {"error": error_message, "phone": phone})

    return render(request, "pay.html")
