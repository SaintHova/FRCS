# Generated by Django 3.1.7 on 2022-01-12 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220112_0024'),
        ('stats', '0025_remove_pit_stats_date_entered'),
    ]

    operations = [
        migrations.AddField(
            model_name='pit_stats',
            name='scout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
