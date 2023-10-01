from django.shortcuts import render

from .models import Dish

# Create your views here.
def index(request):
    data = Dish.objects.order_by('-id')
    cart = request.session.get('cart', None)
    if not cart:
        cart = {}
    request.session['cart'] = cart
    if request.method == 'POST':
        dish_name, dish_count = request.POST.get('dish').split('_')
        request.session['cart'][dish_name] = request.session['cart'].get(dish_name, 0)+int(dish_count)
    return render(request, 'main/main_page.html', {'data': data, 'request': request})

def basket(request):
    return render(request, 'main/basket.html')