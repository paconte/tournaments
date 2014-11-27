# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_auto_20141127_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='tournaments_played',
            field=models.ManyToManyField(to='player.Tournament', null=True, blank=True),
            preserve_default=True,
        ),
    ]
