# noinspection PyPackageRequirements
from django.shortcuts import render, redirect
from .daraja import stk_push
from .models import Payment

from django.shortcuts import render, redirect
from .daraja import stk_push
from .models import Payment

def pay(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        amount = 50

        response = stk_push(phone, amount)

        if response and response.get("ResponseCode") == "0":
            Payment.objects.create(
                phone=phone,
                amount=amount,
                status="INITIATED",
                receipt=response.get("CheckoutRequestID", "")
            )

            request.session["payment_verified"] = True
            return redirect("/predict/")

        return render(request, "pay.html", {
            "error": "Payment initiation failed. Try again."
        })

    return render(request, "pay.html")


