# Generated by Django 5.1.7 on 2025-03-23 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatroom',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
