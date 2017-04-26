# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20170425_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('destination', models.CharField(max_length=100)),
                ('sent', models.BooleanField(default=False)),
                ('retry_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_retry_at', models.DateTimeField(null=True)),
                ('celery_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True, default=''),
        ),
    ]
