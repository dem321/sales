from django import forms
from django.shortcuts import get_object_or_404

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Order, DishOrder, Dish

class OrderForm(forms.ModelForm):

    def save(self, request=None, commit=True):
        m = super(OrderForm, self).save(commit=False)
        if commit:
            m.save()
        for el in request.session['cart']:
            if request.session['cart'][el] > 0:
                print(m.id)
                DishOrder.objects.create(dish=get_object_or_404(Dish, name=el), order=get_object_or_404(Order, id=m.pk), count=int(request.session['cart'][el]))

        del request.session['cart']
        return m
    
    class Meta:
        model = Order
        fields = ('__all__')
        widgets={
            'date': DateTimePickerInput()
        }

        
        