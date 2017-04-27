# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20170427_0302'),
        ('adminapp', '0004_auto_20170427_0603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('kind', models.CharField(max_length=100, blank=True)),
                ('content', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('unread', models.BooleanField(default=True)),
                ('notification', models.ForeignKey(to='adminapp.Notification')),
                ('user', models.ForeignKey(to='mainapp.User')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='users',
            field=models.ManyToManyField(to='mainapp.User', through='adminapp.UserNotification'),
        ),
    ]
