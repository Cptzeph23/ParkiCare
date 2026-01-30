from django.db import models

class Payment(models.Model):
    phone = models.CharField(max_length=15)
    amount = models.IntegerField()
    receipt = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.status}"



