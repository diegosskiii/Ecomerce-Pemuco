"""
Registrar modelos en admin de Django
"""
from django.contrib import admin
from apps.user.models import User, Address, Region

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Region)
