# Generated by Django 4.1.7 on 2024-01-12 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dokon_app', '0005_dokonday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dokonday',
            name='date',
        ),
        migrations.AlterField(
            model_name='dokonday',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dokonday',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
