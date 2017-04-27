# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20170426_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailjob',
            name='status',
            field=models.CharField(max_length=10, default='pending'),
        ),
    ]
