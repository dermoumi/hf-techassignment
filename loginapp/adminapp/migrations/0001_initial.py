# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20170427_0302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('kind', models.CharField(max_length=100, blank=True)),
                ('content', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255, blank=True)),
                ('read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, to='mainapp.User')),
            ],
        ),
    ]
