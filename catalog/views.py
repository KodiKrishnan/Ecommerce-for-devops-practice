from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
    
def product_list(request):
    category_id = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    rating = request.GET.get('rating')

    products = Product.objects.all()
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if rating:
        products = products.filter(review__rating__gte=rating).distinct()

    paginator = Paginator(products, 9)  # 9 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/product_list.html', {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': categories,
    })

# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     return render(request, 'catalog/product_detail.html', {
#         'product': product
#     })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.select_related('user').all()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', slug=product.slug)
    else:
        form = ReviewForm()

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'form': form,
        'reviews': reviews,
    })

