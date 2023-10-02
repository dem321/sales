from django import template
from django.shortcuts import get_object_or_404

from main.models import Dish

register = template.Library()

@register.inclusion_tag('tags/dish.html', takes_context=True)
def dish_display(context, dish):
    context['dish']=dish
    return context

@register.simple_tag
def getattr_template(cart, item):
    if item in cart:
        return cart[item]
    return 0