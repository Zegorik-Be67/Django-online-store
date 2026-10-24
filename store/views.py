from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import Store, Category
from .forms import NewProduct

# The main page of the store
def home(request):
    categories = Category.objects.all()
    store = Store.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        store = store.filter(category__id=category_id)
    search = request.GET.get('search', '').strip()
    if search:
        store = store.filter(Q(title__icontains=search) | Q(description__icontains=search))
    return render(request, 'store/home.html', {'store': store, 'categories': categories, 'search': search})

# Page for adding a new product
def add_product(request):
    if request.method == 'POST':
        products = NewProduct(request.POST, request.FILES)
        if products.is_valid():
            products.save()
            return redirect('store:home')
    else:
        products = NewProduct()

    return render(request, 'store/add_product.html', {'products': products})

# The page for a specific product
def product_id(request, id):
    specific_product = get_object_or_404(Store, id=id)

    return render(request, 'store/product.html', {'specific_product': specific_product})