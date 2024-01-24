# Generated by Django 4.1.7 on 2024-01-19 04:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_user_managers_alter_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='workers', to=settings.AUTH_USER_MODEL),
        ),
    ]