# Generated by Django 2.0 on 2018-05-27 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0009_auto_20180511_1559'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time']},
        ),
    ]
