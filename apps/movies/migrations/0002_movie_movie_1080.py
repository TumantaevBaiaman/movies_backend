# Generated by Django 4.2.5 on 2023-12-29 12:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_1080',
            field=models.FileField(blank=True, null=True, upload_to='origin-movie', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]