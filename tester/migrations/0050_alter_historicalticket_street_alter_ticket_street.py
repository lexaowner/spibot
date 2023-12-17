# Generated by Django 4.2.5 on 2023-12-17 14:30

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0049_shutdown_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalticket',
            name='street',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='district', chained_model_field='district', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tester.street', verbose_name='Улица'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='street',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='district', chained_model_field='district', on_delete=django.db.models.deletion.CASCADE, to='tester.street', verbose_name='Улица'),
        ),
    ]
