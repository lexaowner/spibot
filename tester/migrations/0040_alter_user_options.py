# Generated by Django 4.2.5 on 2023-12-01 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0039_alter_historicalticket_viewed_alter_ticket_viewed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'permissions': [('operator', 'Can add ticket, change, change yourself profile'), ('master', 'Can closed ticked, change owner, change yourself profile'), ('dispatcher', 'Can add ticket, change, change yourself profile, add news, change news, change ticket status')]},
        ),
    ]
