# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-09-14 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LianJiaTenementHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_name', models.CharField(max_length=32, verbose_name='房源名称')),
                ('platform', models.CharField(default='链家网', max_length=3)),
                ('house_message', models.CharField(max_length=64, verbose_name='房源信息')),
                ('price', models.DecimalField(decimal_places=2, default='99999', max_digits=8, verbose_name='租金')),
                ('lon', models.DecimalField(decimal_places=6, max_digits=10, verbose_name='经度')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10, verbose_name='纬度')),
                ('url', models.CharField(max_length=128, verbose_name='具体链接')),
            ],
            options={
                'db_table': 'LianJia_table',
            },
        ),
    ]