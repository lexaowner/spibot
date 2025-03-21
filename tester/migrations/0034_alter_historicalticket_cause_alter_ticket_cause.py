# Generated by Django 4.2.5 on 2023-11-29 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0033_historicalticket_cause_ticket_cause_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalticket',
            name='cause',
            field=models.BooleanField(blank=True, choices=[(True, 'Выполнена'), (False, 'Не дозвон'), (None, 'Отказ')], default=True, null=True, verbose_name='Причина'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='cause',
            field=models.BooleanField(blank=True, choices=[(True, 'Выполнена'), (False, 'Не дозвон'), (None, 'Отказ')], default=True, null=True, verbose_name='Причина'),
        ),
    ]
