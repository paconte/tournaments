# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField(null=True, blank=True)),
                ('local_score', models.SmallIntegerField(null=True, blank=True)),
                ('visitor_score', models.SmallIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.CharField(default=b'Pool A', max_length=16, choices=[(b'Final', b'Final'), (b'Semifinal', b'Semifinal'), (b'1/4', b'1/4'), (b'1/8', b'1/8'), (b'1/16', b'1/16'), (b'Third position', b'Third position'), (b'Fith position', b'Fith position'), (b'Sixth position', b'Sixth position'), (b'Seventh position', b'Seventh position'), (b'Pool A', b'Pool A'), (b'Pool B', b'Pool B'), (b'Pool C', b'Pool C'), (b'Pool D', b'Pool D'), (b'Liga', b'Liga')])),
                ('number_teams', models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('category', models.CharField(default=b'Gold', max_length=6, choices=[(b'Gold', b'Gold'), (b'Silver', b'Silver'), (b'Bronze', b'Bronze'), (b'Wood', b'Wood')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('born', models.DateField(null=True, blank=True)),
                ('nationality', models.CharField(max_length=30, null=True, blank=True)),
                ('gender', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField(null=True, blank=True)),
                ('person', models.ForeignKey(to='player.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerStadistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('assistances', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('game', models.ForeignKey(to='player.Game')),
                ('player', models.ForeignKey(to='player.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('division', models.CharField(max_length=3, choices=[(b'MXO', b'Mixed Open'), (b'MO', b'Mens Open'), (b'WO', b'Womens Open'), (b'SMX', b'Senior Mix Open'), (b'SMO', b'Senior Mens Open'), (b'SWO', b'Senior Womes Open')])),
                ('players', models.ManyToManyField(to='player.Person', through='player.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100, null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('division', models.CharField(max_length=3, choices=[(b'MXO', b'Mixed Open'), (b'MO', b'Mens Open'), (b'WO', b'Womens Open'), (b'SMX', b'Senior Mix Open'), (b'SMO', b'Senior Mens Open'), (b'SWO', b'Senior Womes Open')])),
                ('teams', models.ManyToManyField(to='player.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='player.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='field',
            field=models.ForeignKey(blank=True, to='player.GameField', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='local',
            field=models.ForeignKey(related_name='local', blank=True, to='player.Team', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='phase',
            field=models.ForeignKey(to='player.GameRound'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='tournament',
            field=models.ForeignKey(to='player.Tournament'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='visitor',
            field=models.ForeignKey(related_name='visitor', blank=True, to='player.Team', null=True),
            preserve_default=True,
        ),
    ]
