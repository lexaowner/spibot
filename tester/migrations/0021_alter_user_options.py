# Generated by Django 4.2.5 on 2023-11-07 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0020_alter_news_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'permissions': [('operator', 'Can add ticket, change, change yourself profile'), ('master', 'Can closed ticked, change owner, change yourself profile'), ('dispatcher', 'Can add ticket, change, change yourself profile, add news, change news, change ticket status ')]},
        ),
    ]
