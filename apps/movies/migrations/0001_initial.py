# Generated by Django 4.2.5 on 2023-10-15 18:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('director', '0001_initial'),
        ('genres', '0001_initial'),
        ('actors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='название фильма')),
                ('description', models.TextField(verbose_name='описание')),
                ('release_date', models.DateField(verbose_name='дата выпуска')),
                ('poster', models.ImageField(blank=True, null=True, upload_to='poster', verbose_name='постер')),
                ('movie', models.FileField(upload_to='origin-movie', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания записи')),
                ('is_activ', models.BooleanField(default=True)),
                ('is_free', models.BooleanField(default=False)),
                ('actors', models.ManyToManyField(to='actors.actor', verbose_name='актеры')),
                ('directors', models.ManyToManyField(to='director.director', verbose_name='режиссеры')),
                ('genres', models.ManyToManyField(to='genres.genre', verbose_name='жанры')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
        migrations.CreateModel(
            name='FormatMovie',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quality', models.CharField(max_length=255)),
                ('movie_file', models.FileField(upload_to='movie', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]
