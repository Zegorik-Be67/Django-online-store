from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from .models import Store, Category
from .forms import StoreForm

# Create your views here.

def store_list(request):
    categories = Category.objects.all()
    store = Store.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        store = store.filter(category__id=category_id)
    search = request.GET.get('search', '').strip()
    if search:
        store = store.filter(Q(title__icontains=search) | Q(description__icontains=search))
    return render(request, 'store/home.html', {'store': store, 'categories': categories, 'search': search})

def add_product(request):
    if request.method == 'POST':
        products = StoreForm(request.POST, request.FILES)
        if products.is_valid():
            products.save()
            return redirect('store:store_list')
    else:
        products = StoreForm()

    return render(request, 'store/add_product.html', {'products': products})