from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from bootstrap_datepicker_plus.widgets import DateTimePickerInput, DatePickerInput

from .models import Order, DishOrder, Dish

class OrderForm(forms.ModelForm):

    def save(self, request=None, commit=True):
        m = super(OrderForm, self).save(commit=False)
        if commit:
            m.save()
        order = get_object_or_404(Order, id=m.pk)
        order.user = request.user
        order.save()
        for el in request.session['cart']:
            if request.session['cart'][el] > 0:
                DishOrder.objects.create(dish=get_object_or_404(Dish, name=el), order=order, count=int(request.session['cart'][el]))

        del request.session['cart']
        return m
    
    class Meta:
        model = Order
        fields = ('date', 'employee')
        widgets={
            'date': DateTimePickerInput()
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ReportForm(forms.Form):
    date = forms.DateField(required=True, widget=DatePickerInput())