from django.db import models
from apps.user.models import User
from apps.product.models import Product

class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    sale_date = models.DateField(auto_now_add=True)
    total = models.IntegerField()
    shipping_address = models.CharField(max_length=30, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class SaleDetail(models.Model):
    sale_detail_id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE)