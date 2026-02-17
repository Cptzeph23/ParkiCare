from django.urls import path
from .views import pay
from . import views

urlpatterns = [
     path("pay/", views.pay, name="pay"),
]
