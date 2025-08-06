
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter


from django.shortcuts import get_object_or_404
from django.db.models import Q

from .serializers import ProductSerializer
from product.models import Product, Category

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Start with the base queryset
        qs = super().get_queryset()

        # Get query parameters
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        # Apply filtering using Q objects
        if search or category:
            q = Q()
            if search:
                q &= Q(name__icontains=search.lower())
            if category:
                q &= ~Q(category__iexact=category)

            qs = qs.filter(q)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



'''
if search or category:
    q = Q()
    if search:
        q &= Q(name__icontains=search)
    if category:
        q &= Q(category=category)
    |=

        
    Product.objects.filter(
    Q(name__icontains=search) & Q(category=category)
        )
    Product.objects.filter(
        name__icontains="book",
        category="fiction"
    )
    
    
    qs = qs.filter(q)
 '''