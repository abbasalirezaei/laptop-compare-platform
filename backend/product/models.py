from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Laptop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    # Technical specifications
    ram = models.PositiveIntegerField(help_text="RAM size in GB")
    storage = models.PositiveIntegerField(help_text="Internal storage in GB")
    cpu_model = models.CharField(max_length=100)
    cpu_score = models.PositiveIntegerField(help_text="CPU benchmark score")
    gpu_model = models.CharField(max_length=100, blank=True, null=True)
    screen_size = models.DecimalField(max_digits=4, decimal_places=1, help_text="Screen size in inches")
    battery_capacity = models.PositiveIntegerField(help_text="Battery capacity in mAh")

    def __str__(self):
        return f"{self.brand} - {self.name}"


class LaptopPriceHistory(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.laptop.name} - ${self.price} at {self.recorded_at.date()}"


class LaptopComment(models.Model):
    laptop = models.ForeignKey(
        Laptop,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='laptop_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.laptop.name}'