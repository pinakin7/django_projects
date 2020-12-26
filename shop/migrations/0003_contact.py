# Generated by Django 3.1.4 on 2020-12-23 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20201222_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('phone', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
