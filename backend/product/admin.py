from django.contrib import admin

from .models import  Laptop,LaptopComment,LaptopPriceHistory

admin.site.register(Laptop)
admin.site.register(LaptopComment)
admin.site.register(LaptopPriceHistory)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'discounted_price', 'is_active', 'created_at')
    list_filter = ('brand', 'is_active', 'created_at')
    search_fields = ('name', 'brand')
    ordering = ('-created_at',)