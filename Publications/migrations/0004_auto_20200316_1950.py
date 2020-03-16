# Generated by Django 3.0.4 on 2020-03-16 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Publications', '0003_auto_20200316_1926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ['update_dt'], 'verbose_name': 'Публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AddField(
            model_name='publication',
            name='update_dt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
