from django.urls import path, include
from . import views

app_name = 'product'
urlpatterns = [
    # Define your URL patterns here
    path('', views.laptop_list_view, name='home'),
    path('compare/', views.compare_laptops_view, name='compare-products'),
#     path('api/v1/', include('product.api.v1.urls')),
]
