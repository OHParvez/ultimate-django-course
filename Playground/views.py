from django.shortcuts import render
from Ecommerce.models import Product

def index_page(request):
    product = Product.objects.filter(collection__featured_product_id__isnull = True)
    return render(request, 'index.html', {'product':list(product)})

