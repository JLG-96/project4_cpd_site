# Generated by Django 5.1.6 on 2025-02-11 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0009_remove_team_founded_year_remove_team_home_ground_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerpost',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
