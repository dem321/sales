from django.contrib import admin

from .models import Employee, Dish, Order, DishOrder

# Register your models here.
admin.site.register(Employee)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(DishOrder)