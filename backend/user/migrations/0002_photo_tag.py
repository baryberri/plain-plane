# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-19 04:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/%Y/%m/%d')),
                ('is_reported', models.BooleanField()),
                ('color', django_enumfield.db.fields.EnumField(default=0, enum=user.models.Color)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=5)),
                ('photos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='user.Photo')),
            ],
        ),
    ]
