# myapp/management/commands/generate_products.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from dokon_app.models import ProductType, Product

class Command(BaseCommand):
    help = 'Generates 50 ProductType instances, each with 30 Product instances.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating ProductType instances...'))

        for i in range(1, 11):
            product_type_name = f"ProductType {i}"
            product_type = ProductType.objects.create(name=product_type_name, date=timezone.now())

            self.stdout.write(self.style.SUCCESS(f'ProductType created: {product_type_name}'))

            self.stdout.write(self.style.SUCCESS('Creating Product instances...'))

            for j in range(1, 21):
                product_name = f"Product {j}"
                price = j * 10  # Adjust as needed
                profit_percentage = j + 30  # Adjust as needed
                remain = 100  # Adjust as needed

                Product.objects.create(
                    type=product_type,
                    name=product_name,
                    price=price,
                    profit_percentage=profit_percentage,
                    remain=remain,
                    date=timezone.now()
                )

                self.stdout.write(self.style.SUCCESS(f'Product created: {product_name}'))

        self.stdout.write(self.style.SUCCESS('Generation complete.'))
