from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('store/<int:id>/', views.product_id, name='product_id'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('add_favorite/<int:product_id>', views.add_favorite, name='add_to_favorite'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('register/', views.registration, name='register'),
    path('home/', views.make_order, name='order'),
]