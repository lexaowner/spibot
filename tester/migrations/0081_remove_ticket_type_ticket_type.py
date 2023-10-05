# Generated by Django 4.2.5 on 2023-10-03 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0080_remove_ticket_type_alter_tickettype_type_ticket_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='type',
        ),
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tester.tickettype', verbose_name='Тип заявки'),
        ),
    ]
