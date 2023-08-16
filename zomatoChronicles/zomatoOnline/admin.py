from django.contrib import admin
from .models import CustomUser, Dish, Menu, Order

# Register your models with the admin site
admin.site.register(CustomUser)
admin.site.register(Dish)
admin.site.register(Menu)
admin.site.register(Order)