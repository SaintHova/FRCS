# Generated by Django 3.1.7 on 2022-01-11 17:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20220111_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_buddy_climb',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_control_panel_pos',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_control_panel_rot',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_goal',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='robot_highlow',
        ),
        migrations.RemoveField(
            model_name='pit_stats',
            name='scouted_team_num',
        ),
        migrations.AddField(
            model_name='pit_stats',
            name='incorrect_selection',
            field=models.CharField(default=4, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pit_stats',
            name='robot_goal_height',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pit_stats',
            name='scouting_team',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='date_entered',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 11, 17, 29, 54, 933446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_autonomous',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_climb',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_drivetrain_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_frame_length',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_frame_width',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_vision_implement',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_vision_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pit_stats',
            name='robot_weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]