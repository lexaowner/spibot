# Generated by Django 4.2.5 on 2023-11-08 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0023_alter_historicalticket_street_alter_ticket_street'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalticket',
            name='status',
            field=models.BooleanField(choices=[(True, 'Открыта'), (False, 'Закрыта')], default=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.BooleanField(choices=[(True, 'Открыта'), (False, 'Закрыта')], default=True, verbose_name='Статус'),
        ),
    ]
