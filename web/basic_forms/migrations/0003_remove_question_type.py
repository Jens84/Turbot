# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_forms', '0002_question_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='type',
        ),
    ]
