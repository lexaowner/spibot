# Generated by Django 4.2.5 on 2023-10-10 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0014_alter_ticket_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='operator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='operator_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Оператор'),
        ),
    ]
