# Generated by Django 3.1.7 on 2021-12-05 21:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20211205_2112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_verified',
        ),
        migrations.AddField(
            model_name='profile',
            name='userId',
            field=models.IntegerField(default=4594621),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 5, 21, 14, 5, 884145, tzinfo=utc)),
        ),
    ]
