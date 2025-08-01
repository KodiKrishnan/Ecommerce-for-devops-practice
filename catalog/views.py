from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category

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
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {
        'product': product
    })