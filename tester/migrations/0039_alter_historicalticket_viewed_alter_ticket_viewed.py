# Generated by Django 4.2.5 on 2023-12-01 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0038_historicalticket_date_change_historicalticket_viewed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalticket',
            name='viewed',
            field=models.BooleanField(blank=True, choices=[(True, 'Просмотрено'), (False, 'Не просмотрено')], default=False, null=True, verbose_name='Статус тикета'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='viewed',
            field=models.BooleanField(blank=True, choices=[(True, 'Просмотрено'), (False, 'Не просмотрено')], default=False, null=True, verbose_name='Статус тикета'),
        ),
    ]
