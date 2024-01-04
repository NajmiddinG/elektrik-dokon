# myapp/management/commands/generate_products.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from dokon_app.models import ProductType, Product

class Command(BaseCommand):
    help = 'Delete all the product and producttype data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating ProductType instances...'))
        ProductType.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Generation ProductType delete complete.'))
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Generation Product delete complete.'))

