# Generated by Django 4.2.5 on 2023-12-04 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0004_series_age_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriesvideo',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='количество просмотров'),
        ),
    ]
