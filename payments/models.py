from django.db import models
import razorpay
from account.models import User
# from variations.models import Variation


# Create your models here.

class Order(models.Model):
    choice = (('Approved', 'Approved'), ('Cancelled', 'Cancelled'), ('Cancel', 'Cancel'), ('Pending', 'Pending'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_product = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100, blank=True)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    # variation = models.ForeignKey(Variation, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


