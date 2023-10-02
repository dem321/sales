from django.contrib import admin
from django.urls import path, include

from .views import index, basket, EmployeeAutocomplete, clear_session

urlpatterns = [
    path('', index, name='idx'),
    path('basket', basket, name='basket'),
    path('clear_session', clear_session, name='clear_session'),
    path('employee-autocomplete/', EmployeeAutocomplete.as_view(), name='employee-autocomplete'),
]
