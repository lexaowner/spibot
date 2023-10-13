# Generated by Django 4.2.5 on 2023-10-10 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tester.models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0010_alter_ticket_operator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='operator',
            field=models.ForeignKey(blank=True, default=tester.models.User, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operator_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Оператор'),
        ),
    ]
