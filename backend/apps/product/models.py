from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)
    state = models.BooleanField(default=True)

    class Meta:
        """Meta definition for CategoryProduct."""

        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'

    def __str__(self):
        """Unicode representation of CategoryProduct."""
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=30)
    price = models.IntegerField()
    description = models.CharField(max_length=50)
    stock = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    state = models.BooleanField(default=True)
    image = models.ImageField('Imagen del Producto', upload_to='apps/product/images', blank=True, null=True)

class Opinion(models.Model):
    opinion_id = models.AutoField(primary_key=True)
    evaluation = models.IntegerField()
    commentary = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
