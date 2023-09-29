# Generated by Django 4.2.5 on 2023-09-28 14:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0003_district_region_street_house_district_region_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='closed_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='completion_date',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата выполнения'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата открытия'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='first_contact',
            field=models.CharField(default=None, max_length=13, null=True, verbose_name='Основной номер'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='login',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Логин'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='second_contact',
            field=models.CharField(blank=True, default=None, max_length=13, null=True, verbose_name='Доп. номер'),
        ),
    ]
