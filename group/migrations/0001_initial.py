# Generated by Django 5.0.2 on 2024-03-10 15:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=150)),
                ('teacher', models.CharField(max_length=150)),
                ('exams', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.course')),
                ('student', models.ManyToManyField(related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Groups of students',
            },
        ),
    ]