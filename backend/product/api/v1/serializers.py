from rest_framework import serializers
from product.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')   # Make fields read-only except for those you want to allow writing