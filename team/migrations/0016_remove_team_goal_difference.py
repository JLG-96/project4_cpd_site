# Generated by Django 5.1.6 on 2025-02-16 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0015_team_goal_difference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='goal_difference',
        ),
    ]
