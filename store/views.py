from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from django.db.models import Q
from .models import Store, Category, Order, OrderItem, Review
from .forms import NewProduct, RegistrationForm, ReviewForm


# The main page of the store
def home(request):
    categories = Category.objects.all()
    store = Store.objects.all().order_by('id')
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
@login_required
def product_id(request, id):
    specific_product = get_object_or_404(Store, id=id)

    recent_product = request.session.get('revent_product', [])
    if id in recent_product:
        recent_product.remove(id)
    recent_product.insert(0, id)
    request.session['revent_product'] = recent_product[:5]
    recent_product = Store.objects.filter(id__in=recent_product).exclude(id=id)

    reviews = Review.objects.filter(product=specific_product)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = specific_product
            review.user = request.user
            review.save()
            return redirect('store:product_id', id=specific_product.id)
    else:
        form = ReviewForm()

    return render(request, 'store/product.html', {'specific_product': specific_product, 'recent_product': recent_product, 'reviews': reviews, 'form': form})

@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    request.session['cart'] = cart

    return redirect('store:product_id', product_id)

def remove_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart

    return redirect('store:cart')

@login_required
def cart_view(request):
    product_ids = request.session.get('cart', [])
    products = Store.objects.filter(id__in=product_ids)
    total_price = sum(p.price for p in products)

    return render(request, 'store/cart.html', {'products': products, 'total_price': total_price})

@login_required
def add_favorite(request, product_id):
    favorite_ids = request.session.get('favorite', [])
    if product_id not in favorite_ids:
        favorite_ids.append(product_id)
    request.session['favorite'] = favorite_ids

    return redirect('store:product_id', product_id)

@login_required
def favorites_view(request):
    favorite_ids = request.session.get('favorite', [])
    favorites = Store.objects.filter(id__in=favorite_ids)

    return render(request, 'store/favorites.html', {'favorites': favorites})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('store:home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def make_order(request):
    cart_ids = request.session.get('cart', [])
    if not cart_ids:
        return redirect('store:cart_view')
    products = Store.objects.filter(id__in=cart_ids)
    total_price = sum(p.price for p in products)
    order = Order.objects.create(user=request.user, total_sum=total_price)
    items_to_create = [
        OrderItem(id_order=order, product=p, quantity=1)
        for p in products
    ]
    OrderItem.objects.bulk_create(items_to_create)
    request.session['cart'] = []
    request.session.modified = True

    return redirect('store:cart')