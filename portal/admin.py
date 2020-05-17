from django.contrib import admin

from .models import Product, Policy, Claim

admin.site.register(Product)
admin.site.register(Policy)
admin.site.register(Claim)
