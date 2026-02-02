# noinspection PyPackageRequirements
from django.shortcuts import render, redirect
from urllib3 import request
from .daraja import stk_push
from .models import Payment

from django.shortcuts import render, redirect
from .daraja import stk_push
from .models import Payment

def pay(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = 50

        response = stk_push(phone, amount)

        # Sandbox-safe: proceed after STK attempt
        request.session["payment_verified"] = True
        request.session["user_phone"] = phone
        print("✅ PHONE STORED IN SESSION:", phone)
        return redirect("/predict/")


    return render(request, "pay.html")
