from django.db import models
from datetime import datetime

# Create your models here.
class Transactions(models.Model):
    unique_code = models.CharField(max_length=50,default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(default=datetime.now)
    # image = models.ImageField(upload_to='transactions_images/',null=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.amount} {self.date} "

