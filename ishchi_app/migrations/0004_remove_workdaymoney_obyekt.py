# Generated by Django 4.1.7 on 2024-01-23 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ishchi_app', '0003_workdaymoney_remove_work_date_delete_workday_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workdaymoney',
            name='obyekt',
        ),
    ]
