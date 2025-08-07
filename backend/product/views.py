from django.shortcuts import render
from django.db.models import Q, Max, Min, Count, Avg
from django.http import HttpResponse, HttpResponseBadRequest

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date

from .models import Laptop
from .forms import LaptopCommentForm

def laptop_list_view(request):
    brand = request.GET.get('brand')
    search_query = request.GET.get('search_query')
    price_lte = request.GET.get('price_lte')
    price_gte = request.GET.get('price_gte')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Calculate max and min price for slider
    result = Laptop.objects.aggregate(Max('price'), Min('price'))
    price__max = result.get('price__max') or 0
    price__min = result.get('price__min') or 0

    q = Q(is_active=True)

    if brand:
        q &= Q(brand__iexact=brand)

    if search_query:
        q &= Q(name__icontains=search_query)

    if price_lte:
        try:
            q &= Q(price__lte=float(price_lte))
        except ValueError:
            pass

    if price_gte:
        try:
            q &= Q(price__gte=float(price_gte))
        except ValueError:
            pass

    if start_date:
        parsed_start = parse_date(start_date)
        if parsed_start:
            q &= Q(created_at__date__gte=parsed_start)

    if end_date:
        parsed_end = parse_date(end_date)
        if parsed_end:
            q &= Q(created_at__date__lte=parsed_end)

    laptops = Laptop.objects.filter(q).order_by('-created_at')
    sort_by = request.GET.get('sort_by', 'price')
    valid_sort_fields = ['price', '-price', 'ram', '-ram',
                         'cpu_score', '-cpu_score', 'created_at', '-created_at']

    if sort_by in valid_sort_fields:
        laptops = laptops.order_by(sort_by)

    context = {
        'laptops': laptops,
        'price__max': price__max,
        'price__min': price__min,
        'price_lte': price_lte,
        'price_gte': price_gte,
        'search_query': search_query,
        'brand': brand,
        'start_date': start_date,
        'end_date': end_date,
        'sort_by': sort_by,
    }
    return render(request, 'product/laptop_list.html', context)


def compare_laptops_view(request):
    id1 = request.GET.get('id1')
    id2 = request.GET.get('id2')

    if not id1 or not id2:
        return HttpResponseBadRequest("Please provide both laptop IDs.")

    if id1 == id2:
        return HttpResponseBadRequest("Cannot compare a laptop with itself.")

    try:
        laptop1 = get_object_or_404(Laptop, pk=int(id1))
        laptop2 = get_object_or_404(Laptop, pk=int(id2))
    except ValueError:
        return HttpResponseBadRequest("IDs must be integers.")

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
        'gpu_match': (
            laptop1.gpu_model == laptop2.gpu_model
            if laptop1.gpu_model and laptop2.gpu_model
            else None
        ),
    }

    return render(request, 'product/compare.html', comparison_data)


def admin_dashboard_view(request):
    # Number of laptops by brand
    brand_stats = (
        Laptop.objects.values('brand')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Average price and maximum RAM
    stats = Laptop.objects.aggregate(
        avg_price=Avg('price'),
        max_ram=Max('ram')
    )

    # Most popular laptops based on comment count
    popular_laptops = (
        Laptop.objects.annotate(comment_count=Count('comments'))
        .order_by('-comment_count')[:5]
    )

    context = {
        'brand_stats': brand_stats,
        'avg_price': stats['avg_price'],
        'max_ram': stats['max_ram'],
        'popular_laptops': popular_laptops,
    }
    return render(request, 'product/admin/dashboard.html', context)


@login_required
def laptop_detail_view(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    comments = laptop.comments.select_related('user').order_by('-created_at')
    price_history = laptop.price_history.order_by('recorded_at')

    # تحلیل تعداد کامنت‌ها در زمان
    comment_stats = (
        laptop.comments
        .extra({'date': "date(created_at)"})
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # فرم ارسال کامنت
    if request.method == 'POST':
        form = LaptopCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.laptop = laptop
            new_comment.save()
            return redirect('product:laptop-detail', pk=pk)
    else:
        form = LaptopCommentForm()

    context = {
        'laptop': laptop,
        'comments': comments,
        'price_history': price_history,
        'comment_stats': comment_stats,
        'form': form,
    }
    return render(request, 'product/laptop_detail.html', context)
