# Generated by Django 4.1.7 on 2024-02-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obyekt_app', '0015_obyekt_doc_obyekt'),
    ]

    operations = [
        migrations.AddField(
            model_name='obyekt_doc',
            name='role',
            field=models.CharField(default='ishchi', max_length=100),
        ),
    ]
