from django.shortcuts import render, redirect
from django.http import HttpResponse

from dal import autocomplete

from .models import Dish, Employee
from .forms import OrderForm

class EmployeeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Employee.objects.all()
        if self.q:
            qs = qs.filter(second_name__istartswith=self.q)
        return qs

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
    qs = Dish.objects.all()
    for dish in Dish.objects.all():
        if dish.name not in request.session['cart']:
            qs = qs.exclude(id=dish.id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save(request=request)
        else: return HttpResponse(form.errors)
        return redirect('idx')
    else:
        form=OrderForm()
    return render(request, 'main/basket.html', {'form':form, 'data': qs})

def clear_session(request):
    request.session.flush()
    return redirect('idx')