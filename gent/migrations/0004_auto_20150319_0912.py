# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gent', '0003_auto_20150319_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='family',
            field=models.ForeignKey(related_name=b'items', blank=True, to='gent.Family', null=True),
        ),
    ]
