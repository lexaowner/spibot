from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            permissions_dict = {
                'Опер': 'operator',
                'Мастер': 'master',
                'Диспетчер': 'dispatcher',
            }

            for group, codename in permissions_dict.items():
                permission = Permission.objects.get(codename=codename)
                getattr(Group.objects.get_or_create(name=group)[0], 'permissions').add(permission)

            self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully.'))