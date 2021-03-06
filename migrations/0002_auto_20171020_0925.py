# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-20 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geofence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='cpn',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='geofence.Company'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='cpn',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='geofence.Company'),
        ),
    ]
