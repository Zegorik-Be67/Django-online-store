from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store_list, name='store_list'),
    path('add_product/', views.add_product, name='add_product'),
]