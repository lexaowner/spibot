# Generated by Django 4.2.5 on 2023-10-06 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0090_alter_person_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.CharField(blank=True, choices=[('Новый', 'New'), ('Уже в базе', 'Old')], default=True, max_length=32, null=True, verbose_name='Статус'),
        ),
    ]
