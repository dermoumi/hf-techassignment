# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20170425_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_token',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(verbose_name='username', max_length=100, unique=True, default=''),
        ),
    ]
