# Generated by Django 2.0 on 2018-05-21 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_ex', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_avatar',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
