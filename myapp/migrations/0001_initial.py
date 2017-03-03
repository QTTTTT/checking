# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('late_times', models.IntegerField(default=0)),
                ('early_times', models.IntegerField(default=0)),
                ('up_days', models.IntegerField(default=0)),
                ('down_days', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('identity', models.CharField(max_length=16, unique=True)),
                ('sex', models.CharField(max_length=16)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('first_time', models.TimeField(blank=True, null=True)),
                ('second_time', models.TimeField(blank=True, null=True)),
                ('first_result', models.BooleanField(default=False)),
                ('second_result', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='UserObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('up', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Member')),
            ],
        ),
        migrations.AddField(
            model_name='adminobject',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Member'),
        ),
    ]
