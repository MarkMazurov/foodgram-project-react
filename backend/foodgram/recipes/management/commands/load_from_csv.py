import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Кастомная команда для выгрузки данных из csv-файла"""

    help = 'Загрузка ингредиентов в таблицу'

    def handle(self, *args, **options):
        number = Ingredient.objects.count()
        reader = csv.DictReader(
            open('./data/ingredients.csv'),
            fieldnames=['name', 'measurement_unit']
        )
        Ingredient.objects.bulk_create([Ingredient(**data) for data in reader])
        if (Ingredient.objects.count() > number):
            self.stdout.write(self.style.SUCCESS('Loading complete!'))
        else:
            self.stdout.write(self.style.ERROR('Oops! Crashing!'))
