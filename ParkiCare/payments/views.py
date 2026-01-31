from django.shortcuts import render, redirect
from .daraja import stk_push
from .models import Payment

def pay(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        amount = 50

        response = stk_push(phone, amount)
        print("FINAL RESPONSE:", response)

        return render(request, "pay_wait.html", {
            "response": response
        })

    return render(request, "pay.html")

