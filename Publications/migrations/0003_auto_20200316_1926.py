# Generated by Django 3.0.4 on 2020-03-16 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Publications', '0002_auto_20200316_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='issue',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='publication',
            name='issued',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='publication',
            name='volume',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
