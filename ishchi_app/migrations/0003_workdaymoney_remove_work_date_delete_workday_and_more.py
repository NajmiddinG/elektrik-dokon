# Generated by Django 4.1.7 on 2024-01-21 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('obyekt_app', '0007_obyektjobtype_workamountjobtype'),
        ('ishchi_app', '0002_remove_workday_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDayMoney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earn_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('admin_accepted', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('obyekt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obyekt_app.obyekt')),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='work',
            name='date',
        ),
        migrations.DeleteModel(
            name='WorkDay',
        ),
        migrations.AddField(
            model_name='workdaymoney',
            name='work_amount',
            field=models.ManyToManyField(to='ishchi_app.work'),
        ),
    ]
