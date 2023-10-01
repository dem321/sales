from django.contrib import admin
from django.urls import path, include

from .views import index, basket

urlpatterns = [
    path('', index, name='idx'),
    path('/basket', basket, name='basket')
]
