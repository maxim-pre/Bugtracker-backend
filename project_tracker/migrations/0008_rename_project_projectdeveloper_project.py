# Generated by Django 4.1.2 on 2022-10-27 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_tracker', '0007_rename_projectdevelopers_projectdeveloper'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectdeveloper',
            old_name='Project',
            new_name='project',
        ),
    ]
