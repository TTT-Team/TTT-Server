from django.core.management.base import BaseCommand
from accounts.models import Currency

class Command(BaseCommand):
    help = 'Инициализирует начальные данные в базе данных'

    def handle(self, *args, **options):
        # Создаем рубль, если его еще нет
        if not Currency.objects.filter(code='RUB').exists():
            Currency.objects.create(
                currency='Российский Рубль',
                code='RUB',
                course=0.0,
            )
            self.stdout.write(self.style.SUCCESS('Успешно создана валюта RUB'))
        else:
            self.stdout.write(self.style.SUCCESS('Валюта RUB уже существует')) 