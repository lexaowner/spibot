from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import Region
from django.apps import apps


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if kwargs['app_config'].name == 'tester':
        permissions_dict = {
            'Опер': 'operator',
            'Мастер': 'master',
            'Диспетчер': 'dispatcher',
        }

        for group, codename in permissions_dict.items():
            if codename:
                permission = Permission.objects.get(codename=codename)
                getattr(Group.objects.get_or_create(name=group)[0], 'permissions').add(permission)

        if Region.objects.count() == 0:
            Region.objects.create(name='Ташкент')