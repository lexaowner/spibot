# Generated by Django 4.2.5 on 2024-01-17 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0057_user_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='shutdown',
            name='deleted',
            field=models.BooleanField(blank=True, choices=[(True, 'Удаленна'), (False, 'Активна')], default=False, null=True, verbose_name='Статус_deleted'),
        ),
    ]
