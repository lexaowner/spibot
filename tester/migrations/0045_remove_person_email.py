# Generated by Django 4.2.5 on 2023-10-02 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0044_alter_person_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
    ]
