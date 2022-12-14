# Generated by Django 4.1.3 on 2022-12-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_tracker', '0012_remove_ticket_developer'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('L', 'low'), ('M', 'medium'), ('H', 'high')], default='L', max_length=1),
        ),
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('I', 'issue'), ('B', 'bug'), ('FR', 'feature request')], default='I', max_length=2),
        ),
    ]
