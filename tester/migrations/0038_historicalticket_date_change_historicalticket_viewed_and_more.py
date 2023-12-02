# Generated by Django 4.2.5 on 2023-12-01 12:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0037_alter_historicalticket_cause_alter_ticket_cause'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalticket',
            name='date_change',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата измененя'),
        ),
        migrations.AddField(
            model_name='historicalticket',
            name='viewed',
            field=models.BooleanField(blank=True, choices=[(True, 'Просмотрено'), (False, 'Не просмотрено')], default=False, null=True, verbose_name='Причина'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='date_change',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата измененя'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='viewed',
            field=models.BooleanField(blank=True, choices=[(True, 'Просмотрено'), (False, 'Не просмотрено')], default=False, null=True, verbose_name='Причина'),
        ),
    ]
