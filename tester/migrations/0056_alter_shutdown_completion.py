# Generated by Django 4.2.5 on 2024-01-01 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0055_shutdown_completion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shutdown',
            name='completion',
            field=models.BooleanField(blank=True, choices=[(True, 'Выполнено'), (False, 'Не Выполнено')], default=False, null=True, verbose_name='Выполнение'),
        ),
    ]
