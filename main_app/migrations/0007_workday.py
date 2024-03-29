# Generated by Django 4.1.7 on 2024-01-20 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_worker_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
