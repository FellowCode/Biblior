# Generated by Django 3.0.4 on 2020-03-15 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_auto_20200315_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=64),
        ),
    ]
