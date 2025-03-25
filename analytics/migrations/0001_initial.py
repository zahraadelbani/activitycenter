# Generated by Django 5.1.7 on 2025-03-23 00:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_members', models.PositiveIntegerField(default=0)),
                ('total_events', models.PositiveIntegerField(default=0)),
                ('total_polls', models.PositiveIntegerField(default=0)),
                ('club', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='clubs.club')),
            ],
        ),
    ]
