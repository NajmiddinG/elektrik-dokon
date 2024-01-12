# Generated by Django 4.1.7 on 2024-01-10 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('obyekt_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obyekt_app.workamount')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('earn_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('obyekt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obyekt_app.obyekt')),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('work_amount', models.ManyToManyField(to='ishchi_app.work')),
            ],
        ),
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('given_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('total_earn', models.IntegerField(blank=True, default=0, null=True)),
                ('year', models.IntegerField(default=2023)),
                ('month', models.IntegerField(default=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
