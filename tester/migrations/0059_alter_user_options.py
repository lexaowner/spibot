# Generated by Django 4.2.5 on 2024-01-19 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0058_shutdown_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'permissions': [('base', 'Just watch'), ('operator', 'Can add ticket, change, change yourself profile'), ('master', 'Can closed ticked, change owner, change yourself profile'), ('dispatcher', 'Can add ticket, change, change yourself profile, add news, change news, change ticket status')], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
