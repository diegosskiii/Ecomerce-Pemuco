from django.contrib import admin
from apps.cart.models import *

admin.site.register(Cart)
admin.site.register(CartDetail)
admin.site.register(CartState)
