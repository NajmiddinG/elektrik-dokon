# Generated by Django 4.1.7 on 2024-01-16 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obyekt_app', '0003_obyekt_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obyekt',
            name='work_amount',
            field=models.ManyToManyField(blank=True, null=True, to='obyekt_app.workamount'),
        ),
    ]
