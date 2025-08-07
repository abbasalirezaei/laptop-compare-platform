from django.urls import path, include
from . import views

app_name = 'product'
urlpatterns = [
    # Define your URL patterns here
    path('', views.laptop_list_view, name='home'),
    path('compare/', views.compare_laptops_view, name='compare-products'),
    path('product/admin/', views.admin_dashboard_view, name='admin-dashboard'),
    path('product/<int:pk>/', views.laptop_detail_view, name='laptop-detail'), 
]
