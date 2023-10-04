from django import template
from django.shortcuts import get_object_or_404

from main.models import Dish, DishOrder, Order

register = template.Library()

@register.inclusion_tag('tags/dish.html', takes_context=True)
def dish_display(context, dish):
    context['dish']=dish
    return context

@register.simple_tag
def get_basket_count(cart, item):
    if item in cart:
        return cart[item]
    return 0

@register.simple_tag
def get_price(dish, cart):
    return (dish.price * int(get_basket_count(cart, dish.name)))

@register.inclusion_tag('tags/history_dish.html')
def history_dish_display(order):
    order = DishOrder.objects.filter(order=order)
    return {'order':order}

@register.simple_tag
def get_report_data(table, dish, obj):
    return table[dish][obj]