# Generated by Django 2.0.2 on 2018-03-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20180306_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
    ]
