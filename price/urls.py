from django.urls import path,include
from . import views

urlpatterns = [
    path('fetch_price', views.fetch_price, name="fetch_price"),
    path('list_price', views.list_price, name="list_price"),
]