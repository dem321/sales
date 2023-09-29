from django import template
from django.shortcuts import get_object_or_404

from main.models import Dish

register = template.Library()

@register.inclusion_tag('tags/dish.html')
def dish_display(dish):
    return {'dish': dish}