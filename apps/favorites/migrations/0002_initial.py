# Generated by Django 4.2.5 on 2023-12-20 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('favorites', '0001_initial'),
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='series',
            field=models.ManyToManyField(to='series.series'),
        ),
    ]
