# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_auto_20170427_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='users',
        ),
        migrations.RemoveField(
            model_name='usernotification',
            name='notification',
        ),
        migrations.RemoveField(
            model_name='usernotification',
            name='user',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
        migrations.DeleteModel(
            name='UserNotification',
        ),
    ]
