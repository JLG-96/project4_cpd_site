# Generated by Django 5.1.5 on 2025-02-08 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_remove_playeravailability_available_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playeravailability',
            old_name='match_fixture',
            new_name='fixture',
        ),
        migrations.RemoveField(
            model_name='playeravailability',
            name='training_session',
        ),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
