# Generated by Django 5.1.6 on 2025-03-02 17:38

import django.db.models.deletion
import students.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.IntegerField()),
                ('subjects', models.JSONField()),
                ('backlogs', models.JSONField(default=list)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_marks', models.JSONField(default=dict)),
                ('weakest_subjects', models.JSONField(default=list)),
                ('easiest_subjects', models.JSONField(default=list)),
                ('preferred_learning_style', models.CharField(max_length=50)),
                ('study_goal', models.CharField(max_length=100)),
                ('available_study_hours', models.JSONField(default=students.models.default_study_hours)),
                ('personality_type', models.CharField(max_length=50)),
                ('primary_language', models.CharField(max_length=50)),
                ('preferred_collaboration_tools', models.JSONField(default=list)),
                ('preferred_study_environment', models.CharField(max_length=50)),
                ('geographical_proximity', models.CharField(blank=True, max_length=50, null=True)),
                ('communication_style', models.CharField(max_length=50)),
                ('motivational_level', models.CharField(max_length=50)),
                ('preferred_study_time', models.CharField(max_length=50)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
