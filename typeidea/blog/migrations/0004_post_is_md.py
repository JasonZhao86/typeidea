# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-23 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_content_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_md',
            field=models.BooleanField(default=False, verbose_name='是否使用markdown语法'),
        ),
    ]
