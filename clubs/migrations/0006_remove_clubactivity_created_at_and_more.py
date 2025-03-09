# Generated by Django 5.1.1 on 2025-03-08 20:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_announcement_visible'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubactivity',
            name='created_at',
        ),
        migrations.AddField(
            model_name='clubactivity',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='clubactivity',
            name='approval_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='clubactivity',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club'),
        ),
        migrations.AlterField(
            model_name='clubactivity',
            name='needs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clubactivity',
            name='supporting_documents',
            field=models.FileField(blank=True, null=True, upload_to='activity_docs/'),
        ),
        migrations.AlterField(
            model_name='clubactivity',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
