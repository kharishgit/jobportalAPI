# Generated by Django 4.1.1 on 2022-11-08 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='time_period',
            field=models.IntegerField(blank=True, default=3, null=True),
        ),
    ]
