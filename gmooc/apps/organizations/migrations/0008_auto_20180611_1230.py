# Generated by Django 2.0.2 on 2018-06-11 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_courseorg_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='organizations/%Y/%m', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(upload_to='teachers/%Y/%m', verbose_name='头像'),
        ),
    ]