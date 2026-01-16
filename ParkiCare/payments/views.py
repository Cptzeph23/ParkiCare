from django.shortcuts import render, redirect
from .daraja import stk_push
from .models import Payment

def pay(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        amount = 50

        Payment.objects.create(phone=phone, amount=amount)
        stk_push(phone, amount)

        return render(request, "pay_wait.html")

    return render(request, "pay.html")

