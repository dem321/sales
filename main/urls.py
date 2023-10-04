from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='idx'),
    path('basket', views.basket, name='basket'),
    path('clear_session', views.clear_session, name='clear_session'),
    path('profile', views.profile, name='profile'),
    path('registration', views.register, name='registration'),
    path('login', views.login_view, name='login'),
    path('report', views.report, name='report'),
    path('employee-autocomplete/', views.EmployeeAutocomplete.as_view(), name='employee-autocomplete'),
]
