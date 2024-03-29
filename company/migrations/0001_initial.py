# Generated by Django 4.1.1 on 2022-11-07 06:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('size', models.CharField(max_length=20)),
                ('founded', models.CharField(max_length=10)),
                ('stage', models.CharField(max_length=20)),
                ('about', models.TextField(null=True)),
                ('linked_in', models.URLField()),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
