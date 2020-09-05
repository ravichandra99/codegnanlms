from django.db import models

from authentication.models import MyUser

from lms.models import Course, OnlineClassroom

# Create your models here.


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    amount = models.IntegerField()
    amount_paid = models.IntegerField()
    amount_due = models.IntegerField()
    currency = models.CharField(max_length=100)
    receipt_no = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    attempts = models.IntegerField()
    notes = models.TextField()
    created_at = models.CharField(max_length=100)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    online_class = models.ForeignKey(OnlineClassroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id


class Checkout(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100)
    razorpay_signature = models.CharField(max_length=100)
    successful = models.NullBooleanField()
