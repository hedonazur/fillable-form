from django.contrib import admin
from .models import Client, Product, Proforma, Settings


# Register your models here.
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Proforma)
admin.site.register(Settings)