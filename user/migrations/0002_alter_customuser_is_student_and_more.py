# Generated by Django 5.0.2 on 2024-03-10 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_student',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(null=True),
        ),
    ]
