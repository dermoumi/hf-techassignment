# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20170426_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailjob',
            name='sent',
        ),
        migrations.AddField(
            model_name='emailjob',
            name='status',
            field=models.CharField(max_length=10, default='pending', choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')]),
        ),
    ]
