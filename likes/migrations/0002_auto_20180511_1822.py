# Generated by Django 2.0 on 2018-05-11 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likerecord',
            options={'ordering': ['-liked_time']},
        ),
    ]
