# Generated by Django 3.1.7 on 2022-01-12 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0012_auto_20220112_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_autonomous',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_climb',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_drivetrain_type',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_goal_height',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_vision_implement',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_vision_type',
        ),
    ]