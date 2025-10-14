from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    q = request.GET.get('q')
    products = Product.objects.all().order_by('-created_at')
    if q:
        products = products.filter(name__icontains=q)
    context = {'products': products}
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
