# Generated by Django 4.1.7 on 2024-01-25 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ishchi_app', '0004_remove_workdaymoney_obyekt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workdaymoney',
            name='work_amount',
            field=models.ManyToManyField(blank=True, to='ishchi_app.work'),
        ),
    ]
