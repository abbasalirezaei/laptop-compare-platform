from django.shortcuts import render
from django.db.models import Q, Max, Min
from django.http import HttpResponse
from .models import Laptop

def laptop_list_view(request):
    # دریافت پارامترهای فیلتر
    brand = request.GET.get('brand')
    search_query = request.GET.get('search_query')
    price_lte = request.GET.get('price_lte')
    price_gte = request.GET.get('price_gte')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # محاسبه بیشترین و کمترین قیمت برای اسلایدر
    result = Laptop.objects.aggregate(Max('price'), Min('price'))
    price__max = result.get('price__max', 0)
    price__min = result.get('price__min', 0)

    laptops = Laptop.objects.all()
    q = Q()

    if brand:
        q &= Q(brand__iexact=brand)
    if search_query:
        q &= Q(name__icontains=search_query)
    if price_lte:
        try:
            q &= Q(price__lte=float(price_lte))
        except (ValueError, TypeError):
            pass
    if price_gte:
        try:
            q &= Q(price__gte=float(price_gte))
        except (ValueError, TypeError):
            pass
    if start_date:
        q &= Q(created_at__gte=start_date)
    if end_date:
        q &= Q(created_at__lte=end_date)

    laptops = laptops.filter(q)

    context = {
        'laptops': laptops,
        'price__max': price__max,
        'price__min': price__min,
        'price_lte': price_lte,
    }
    return render(request, 'product/laptop_list.html', context)





from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Laptop

def compare_laptops_view(request):
    id1 = request.GET.get('id1')
    id2 = request.GET.get('id2')

    if not id1 or not id2:
        return HttpResponse("Please provide both laptop IDs", status=400)

    laptop1 = get_object_or_404(Laptop, pk=id1)
    laptop2 = get_object_or_404(Laptop, pk=id2)

    comparison_data = {
        'product1': laptop1,
        'product2': laptop2,
        'price_difference': abs(laptop1.price - laptop2.price),
        'discount_diff': abs(laptop1.discounted_price - laptop2.discounted_price),
        'created_diff_days': abs((laptop1.created_at - laptop2.created_at).days),
        'ram_diff': abs(laptop1.ram - laptop2.ram),
        'storage_diff': abs(laptop1.storage - laptop2.storage),
        'cpu_score_diff': abs(laptop1.cpu_score - laptop2.cpu_score),
        'battery_diff': abs(laptop1.battery_capacity - laptop2.battery_capacity),
        'same_brand': laptop1.brand == laptop2.brand,
    }

    return render(request, 'product/compare.html', comparison_data)