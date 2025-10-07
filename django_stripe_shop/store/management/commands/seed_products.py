from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = "Seed 3 example products"

    def handle(self, *args, **options):
        products = [
            {"name": "Red T-shirt", "price_cents": 1500},
            {"name": "Blue Mug", "price_cents": 999},
            {"name": "Sticker Pack", "price_cents": 299},
        ]
        for p in products:
            obj, created = Product.objects.get_or_create(name=p["name"], defaults={"price_cents": p["price_cents"]})
            if not created:
                obj.price_cents = p["price_cents"]
                obj.save()
        self.stdout.write(self.style.SUCCESS("Seeded products."))
