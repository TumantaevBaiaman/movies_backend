# Generated by Django 4.2.5 on 2023-10-18 11:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actors', '0001_initial'),
        ('director', '0001_initial'),
        ('genres', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesVideo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('series', models.FileField(upload_to='series-video', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('release_date', models.DateField(verbose_name='дата выпуска')),
                ('object_id', models.UUIDField()),
                ('is_activ', models.BooleanField(default=True)),
                ('is_free', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Сериал видео',
                'verbose_name_plural': 'Сериалы видео',
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='название фильма')),
                ('description', models.TextField(verbose_name='описание')),
                ('poster', models.ImageField(blank=True, null=True, upload_to='poster', verbose_name='постер')),
                ('release_date', models.DateField(verbose_name='дата выпуска')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания записи')),
                ('is_activ', models.BooleanField(default=True)),
                ('is_free', models.BooleanField(default=False)),
                ('actors', models.ManyToManyField(to='actors.actor', verbose_name='актеры')),
                ('directors', models.ManyToManyField(to='director.director', verbose_name='режиссеры')),
                ('genres', models.ManyToManyField(to='genres.genre', verbose_name='жанры')),
            ],
            options={
                'verbose_name': 'Сериал',
                'verbose_name_plural': 'Сериалы',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('season', models.IntegerField()),
                ('release_date', models.DateField(verbose_name='дата выпуска')),
                ('is_activ', models.BooleanField(default=True)),
                ('is_free', models.BooleanField(default=False)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.series')),
            ],
            options={
                'verbose_name': 'Сезон',
                'verbose_name_plural': 'Сезоны',
            },
        ),
    ]