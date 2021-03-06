# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-24 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0005_auto_20160310_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameround',
            name='round',
            field=models.CharField(choices=[('Final', 'Final'), ('Semifinal', 'Semifinal'), ('1/4', '1/4'), ('Eighthfinals', 'Eighthfinals'), ('1/16', '1/16'), ('Third position', 'Third position'), ('Fifth position', 'Fifth position'), ('Sixth position', 'Sixth position'), ('Seventh position', 'Seventh position'), ('Eighth position', 'Eighth position'), ('Ninth position', 'Ninth position'), ('Tenth position', 'Tenth position'), ('Eleventh position', 'Eleventh position'), ('Twelfth position', 'Twelfth position'), ('Thirteenth position', 'Thirteenth position'), ('Fifteenth position', 'Fifteenth position'), ('Sixteenth position', 'Sixteenth position'), ('Eighteenth position', 'Eighteenth position'), ('Twentieth position', 'Twentieth position'), ('Division', 'Division'), ('Pool A', 'Pool A'), ('Pool B', 'Pool B'), ('Pool C', 'Pool C'), ('Pool D', 'Pool D'), ('Pool E', 'Pool E'), ('Pool F', 'Pool F'), ('Liga', 'Liga')], default='Pool A', max_length=32),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', None)], default='U', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='division',
            field=models.CharField(choices=[('MXO', 'Mixed Open'), ('MO', 'Mens Open'), ('WO', 'Womens Open'), ('SMX', 'Senior Mix Open'), ('SMO', 'Senior Mens Open'), ('SWO', 'Senior Womes Open'), ('W27', 'Women 27')], max_length=3),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='division',
            field=models.CharField(choices=[('MXO', 'Mixed Open'), ('MO', 'Mens Open'), ('WO', 'Womens Open'), ('SMX', 'Senior Mix Open'), ('SMO', 'Senior Mens Open'), ('SWO', 'Senior Womes Open'), ('W27', 'Women 27')], max_length=3),
        ),
    ]
