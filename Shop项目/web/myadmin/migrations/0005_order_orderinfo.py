# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-25 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=255)),
                ('totalprice', models.FloatField()),
                ('status', models.IntegerField(default=0)),
                ('paytype', models.IntegerField(default=0)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('paytime', models.DateTimeField(null=True)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('goodsid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Goods')),
                ('orderid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Order')),
            ],
        ),
    ]
