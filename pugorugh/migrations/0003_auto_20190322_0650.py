# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-22 03:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0002_auto_20190322_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='image_filename',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]