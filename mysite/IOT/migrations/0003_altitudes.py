# Generated by Django 5.2 on 2025-04-07 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IOT', '0002_pressures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Altitudes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IOT.devices')),
            ],
        ),
    ]
