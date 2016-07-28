# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_team_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['gender', 'last_name', 'first_name']},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['person']},
        ),
        migrations.RemoveField(
            model_name='playerstadistic',
            name='assistances',
        ),
        migrations.AddField(
            model_name='playerstadistic',
            name='mvp',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='playerstadistic',
            name='played',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='playerstadistic',
            name='tournament',
            field=models.ForeignKey(to='player.Tournament', null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='number',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='playerstadistic',
            name='game',
            field=models.ForeignKey(to='player.Game', null=True),
        ),
        migrations.AlterField(
            model_name='playerstadistic',
            name='points',
            field=models.PositiveSmallIntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='division',
            field=models.CharField(max_length=3, choices=[(b'MXO', b'Mixed Open'), (b'MO', b'Mens Open'), (b'WO', b'Womens Open'), (b'SMX', b'Senior Mix Open'), (b'M30', b'Mens 30'), (b'M40', b'Mens 40'), (b'W27', b'Women 27')]),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='division',
            field=models.CharField(max_length=3, choices=[(b'MXO', b'Mixed Open'), (b'MO', b'Mens Open'), (b'WO', b'Womens Open'), (b'SMX', b'Senior Mix Open'), (b'M30', b'Mens 30'), (b'M40', b'Mens 40'), (b'W27', b'Women 27')]),
        ),
    ]
