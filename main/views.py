from django.shortcuts import render

from .models import Dish

# Create your views here.
def index(request):
    data = Dish.objects.order_by('-id')
    return render(request, 'main/main_page.html', {'data': data})