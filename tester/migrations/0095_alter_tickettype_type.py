# Generated by Django 4.2.5 on 2023-10-06 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0094_alter_tickettype_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettype',
            name='type',
            field=models.CharField(blank=True, choices=[(None, 'Ремонт'), ('settings', 'Настройка'), ('transfer', 'Перенос'), ('shutdown', 'Отключение'), ('installation', 'Установка')], default=None, max_length=32, null=True, verbose_name='Тип заявки'),
        ),
    ]
