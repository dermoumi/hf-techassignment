# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20170427_0302'),
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('unread', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='notification',
            name='read',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='usernotification',
            name='notification',
            field=models.ForeignKey(to='adminapp.Notification'),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='user',
            field=models.ForeignKey(to='mainapp.User'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ManyToManyField(to='mainapp.User', through='adminapp.UserNotification'),
        ),
    ]
