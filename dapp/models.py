import email
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_name=models.CharField(max_length=200)
    product_price=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    payment_id=models.CharField(max_length=100)
    paid=models.BooleanField(default=False)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    