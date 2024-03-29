# Generated by Django 4.1.7 on 2024-01-29 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('obyekt_app', '0009_workamount_visible_obyekt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Given_money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('obyekt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obyekt_app.obyekt')),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
