# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-03-19 03:27
from __future__ import unicode_literals

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
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image_filename', models.ImageField(blank=True, upload_to='')),
                ('breed', models.CharField(blank=True, max_length=255)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=1)),
                ('size', models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('l', 'liked'), ('d', 'disliked')], max_length=1)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userdog', to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(choices=[('b', 'baby'), ('y', 'young'), ('a', 'adult'), ('s', 'senior')], default='b,y,a,s', max_length=1)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], default='m,f', max_length=1)),
                ('size', models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large')], default='s,m,l,xl', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
