# Generated by Django 4.2.5 on 2023-11-09 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0024_alter_historicalticket_status_alter_ticket_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AlterField(
            model_name='historicalticket',
            name='status',
            field=models.BooleanField(blank=True, choices=[(True, 'Открыта'), (False, 'Закрыта')], default=None, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.BooleanField(blank=True, choices=[(True, 'Открыта'), (False, 'Закрыта')], default=None, null=True, verbose_name='Статус'),
        ),
    ]
