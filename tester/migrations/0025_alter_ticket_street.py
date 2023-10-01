# Generated by Django 4.2.5 on 2023-09-30 14:21

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0024_alter_ticket_street'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='street',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='district', chained_model_field='district', null=True, on_delete=django.db.models.deletion.CASCADE, to='tester.street'),
        ),
    ]
