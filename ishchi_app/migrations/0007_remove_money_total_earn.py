# Generated by Django 4.1.7 on 2024-02-01 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ishchi_app', '0006_remove_money_month_remove_money_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='money',
            name='total_earn',
        ),
    ]