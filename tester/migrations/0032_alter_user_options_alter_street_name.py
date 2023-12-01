# Generated by Django 4.2.5 on 2023-11-28 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0031_shutdown'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'permissions': [('operator', 'Can add ticket, change, change yourself profile'), ('master', 'Can closed ticked, change owner, change yourself profile'), ('', 'Can add ticket, change, change yourself profile, add news, change news, change ticket status')]},
        ),
        migrations.AlterField(
            model_name='street',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Улица'),
        ),
    ]
