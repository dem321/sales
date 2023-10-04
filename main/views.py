from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from dal import autocomplete

from datetime import datetime

from .models import Dish, Employee, Order, DishOrder
from .forms import OrderForm, RegistrationForm, ReportForm

class EmployeeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Employee.objects.all()
        if self.q:
            qs = qs.filter(second_name__istartswith=self.q)
        return qs

def index(request):
    data = Dish.objects.order_by('-id')
    cart = request.session.get('cart', None)
    if not cart:
        cart = {}
    request.session['cart'] = cart
    if request.method == 'POST':
        dish_name, dish_count = request.POST.get('dish').split('_')
        if request.session['cart'].get(dish_name, 0)+int(dish_count) >= 0:
            request.session['cart'][dish_name] = request.session['cart'].get(dish_name, 0)+int(dish_count)
    return render(request, 'main/main_page.html', {'data': data, 'request': request})

def basket(request):
    qs = Dish.objects.all()
    for dish in Dish.objects.all():
        if dish.name not in request.session['cart'] or request.session['cart'].get(dish.name, 0) < 1:
            qs = qs.exclude(id=dish.id)
    if request.method == 'POST':
        if 'dish' in request.POST:
            dish_name, dish_count = request.POST.get('dish').split('_')
            if request.session['cart'][dish_name]+int(dish_count) >= 0:
                request.session['cart'][dish_name] = request.session['cart'][dish_name]+int(dish_count)
            form=OrderForm()    
        else:
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save(request=request)
            else: return HttpResponse(form.errors)
            return redirect('idx')
    else: 
        form=OrderForm()
    return render(request, 'main/basket.html', {'form':form, 'data': qs})

def clear_session(request):
    del request.session['cart']
    return redirect('idx') 

def profile(request):
    orders = Order.objects.filter(user=request.user)          
    return render(request, 'main/profile.html', {'orders':orders})

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("idx")
    form = RegistrationForm()
    return render (request, "main/register.html", {"form":form})

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Вы вошли как {username}.")
				return redirect("idx")
			else:
				messages.error(request,"Неверное имя пользователя или пароль")
		else:
			messages.error(request,"Неверное имя пользователя или пароль")
	form = AuthenticationForm()
	return render(request, "main/login.html", {"form":form})

def report(request):
    table = {}
    total = 0
    if 'date' in request.GET:
        date = datetime.strptime(request.GET['date'], '%Y-%m-%d')
        orders = Order.objects.filter(date__year=date.strftime('%Y'), date__month=date.strftime('%m'), date__day=date.strftime('%d') )
        for order in orders:
            dishes = DishOrder.objects.filter(order=order)
            for dish in dishes:
                if dish.dish in table:
                    table[dish.dish]['count'] += dish.count
                else:
                    table[dish.dish] = {}
                    table[dish.dish]['count'] = dish.count
                    table[dish.dish]['price'] = dish.dish.price
        for dish in table:
            table[dish]['total'] = int(table[dish]['count']) * int(table[dish]['price'])
            total += table[dish]['total']
    form = ReportForm()
    print(table)
    return render (request, "main/report.html", {"form":form, 'table':table, 'total':total})
