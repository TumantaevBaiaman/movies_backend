# Generated by Django 4.2.5 on 2023-12-07 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0005_seriesvideo_views'),
        ('watch_history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchhistory',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='series.seriesvideo'),
        ),
    ]
