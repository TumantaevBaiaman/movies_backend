from django.core.files import File
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.movies.models import Movie, FormatMovie
from apps.movies.serializers import MovieSerializer, FormatMovieSerializer, MovieViewSerializer
from movies_backend.decorators import is_admin_decorator_detail, is_admin_decorator

import ffmpeg
from moviepy.editor import VideoFileClip
import subprocess


def save_format_movie(video_file, movie):
    # Получить путь к временному файлу
    video_path = video_file.temporary_file_path()

    # Создать экземпляр VideoFileClip из временного файла
    video_clip = VideoFileClip(video_path)

    # Качество 720p
    output_720p = "static/output_720p.mp4"
    video_clip.resize(width=1280).write_videofile(output_720p)

    # Качество 1080p
    output_1080p = "static/output_1080p.mp4"
    video_clip.resize(width=1920).write_videofile(output_1080p)

    # Создать записи FormatMovie
    with default_storage.open('output_720p.mp4', "rb") as file:
        django_file_720 = File(file)
    with default_storage.open('output_1080p.mp4', "rb") as file:
        django_file_1080 = File(file)
    FormatMovie.objects.create(movie=movie, quality="720p", movie_file=django_file_720).save()
    FormatMovie.objects.create(movie=movie, quality="1080p", movie_file=django_file_1080).save()


def list_movies(request):
    movies = Movie.objects.all()
    serializer = MovieViewSerializer(instance=movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def detail_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    serializer = MovieViewSerializer(instance=movie)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_movie_genre(request, id_genre):
    movies = Movie.objects.filter(genres__id=id_genre)
    serializer = MovieViewSerializer(instance=movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_movie_recommendation(request, id_genre):
    movies = Movie.objects.filter(genres__id=id_genre)[:10]
    serializer = MovieViewSerializer(instance=movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@is_admin_decorator_detail
def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@is_admin_decorator_detail
def put_movie(request, id): # noqa
    movie = get_object_or_404(Movie, id=id) # noqa
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator_detail
def path_movie(request, id):    # noqa
    movie = get_object_or_404(Movie, id=id) # noqa
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator
def create_movie(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        movie = serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)