# Generated by Django 4.2.5 on 2023-10-12 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_file',
            field=models.FileField(default=1, upload_to='movie_files', verbose_name='Фильм'),
            preserve_default=False,
        ),
    ]
