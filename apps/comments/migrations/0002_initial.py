# Generated by Django 4.2.5 on 2023-12-20 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentseries',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.series'),
        ),
    ]
