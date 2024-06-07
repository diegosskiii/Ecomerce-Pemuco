from django.db import models
from apps.product.models import Product

class Cart_state(models.Model):
    cart_state_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=30, blank=True, null=True)

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    creation_date = models.DateField(auto_now_add=True)
    total_price_cart = models.IntegerField()
    cart_state = models.ForeignKey(Cart_state, on_delete=models.CASCADE)

class Cart_detail(models.Model):
    cart_detail_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)