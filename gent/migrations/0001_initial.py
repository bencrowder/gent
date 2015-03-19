# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('husband_name', models.CharField(max_length=250, verbose_name=b'Husband: Name', blank=True)),
                ('husband_id', models.CharField(max_length=50, verbose_name=b'Husband: FamilyTree ID', blank=True)),
                ('wife_name', models.CharField(max_length=250, verbose_name=b'Wife: Name', blank=True)),
                ('wife_id', models.CharField(max_length=50, verbose_name=b'Wife: FamilyTree ID', blank=True)),
                ('notes', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'families',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('completed', models.BooleanField(default=False)),
                ('date_completed', models.DateTimeField(null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
                ('family', models.ForeignKey(related_name=b'items', to='gent.Family')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(related_name=b'items', null=True, to='gent.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='tags',
            field=models.ManyToManyField(related_name=b'families', null=True, to='gent.Tag', blank=True),
            preserve_default=True,
        ),
    ]
