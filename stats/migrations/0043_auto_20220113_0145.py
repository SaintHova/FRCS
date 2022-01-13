# Generated by Django 3.1.7 on 2022-01-13 01:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0042_auto_20220112_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pit_stats',
            name='date_entered',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 13, 1, 44, 59, 856392, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='stat_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
