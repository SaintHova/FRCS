# Generated by Django 3.1.7 on 2022-01-11 22:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_auto_20220111_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pit_stats',
            name='date_entered',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 11, 22, 43, 3, 239688, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='incorrect_selection',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='is_incorrect',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='notes',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_frame_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_frame_width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]