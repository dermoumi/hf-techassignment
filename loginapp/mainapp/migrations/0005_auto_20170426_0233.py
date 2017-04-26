# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20170426_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailjob',
            name='celery_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
