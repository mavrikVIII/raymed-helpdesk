# Generated by Django 3.2.3 on 2021-09-20 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raymedasset', '0002_alter_person_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='internal_number_phone',
        ),
        migrations.RemoveField(
            model_name='person',
            name='number_pasport',
        ),
        migrations.RemoveField(
            model_name='person',
            name='number_phone',
        ),
        migrations.RemoveField(
            model_name='person',
            name='serial_pasport',
        ),
    ]
