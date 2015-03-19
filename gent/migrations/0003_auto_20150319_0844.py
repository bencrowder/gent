# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gent', '0002_tag_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='starred',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='starred',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
