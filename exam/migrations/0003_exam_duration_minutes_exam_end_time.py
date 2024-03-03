# Generated by Django 5.0.2 on 2024-03-03 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_alter_option_option_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='duration_minutes',
            field=models.PositiveIntegerField(default=60),
        ),
        migrations.AddField(
            model_name='exam',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]