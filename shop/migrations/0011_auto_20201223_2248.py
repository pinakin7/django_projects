# Generated by Django 3.1.4 on 2020-12-23 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_orders_phone'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
    ]
