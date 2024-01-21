from django.core.management.base import BaseCommand
from tester.models import User
from django.db import transaction


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        with transaction.atomic():
            username = 'owner'  # Логин суперпользователя
            email = 'admin@example.com'  # Email суперпользователя
            password = '1234'  # Пароль суперпользователя (можете изменить на свой)

            # Проверяем, существует ли пользователь с таким логином
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))