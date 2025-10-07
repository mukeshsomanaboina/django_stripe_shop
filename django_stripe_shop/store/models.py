from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price_cents = models.IntegerField(help_text="Price in cents (e.g., $5.00 -> 500)")

    def price_decimal(self):
        return self.price_cents / 100

    def __str__(self):
        return f"{self.name} (${self.price_decimal():.2f})"


class Order(models.Model):
    client_token = models.CharField(max_length=64, unique=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    stripe_session_url = models.TextField(blank=True, null=True)
    items = models.JSONField(default=list)  # list of {product_id, name, qty, unit_price_cents}
    total_cents = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_decimal(self):
        return self.total_cents / 100

    def __str__(self):
        return f"Order {self.id} - ${self.total_decimal():.2f} - paid={self.paid}"
