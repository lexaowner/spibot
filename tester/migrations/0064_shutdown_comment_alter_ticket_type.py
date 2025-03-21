# Generated by Django 4.2.5 on 2024-02-06 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0063_alter_shutdown_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='shutdown',
            name='comment',
            field=models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Комментарий мастера'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('Ремонт', 'Ремонт'), ('Настройка', 'Настройка'), ('Перенос', 'Перенос'), ('Включение', 'Включение'), ('Отключение', 'Отключение'), ('Установка', 'Установка'), ('Тюнер', 'Тюнер')], max_length=13, verbose_name='Тип заявки'),
        ),
    ]
