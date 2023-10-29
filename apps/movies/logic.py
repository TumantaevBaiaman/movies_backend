import io
import os
import tempfile

from django.core.files import File
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.genres.models import Genre
from apps.movies.models import Movie, FormatMovie
from apps.movies.serializers import MovieSerializer, FormatMovieSerializer, MovieViewSerializer
from movies_backend.decorators import is_admin_decorator_detail, is_admin_decorator

# from moviepy.editor import VideoFileClip
# import subprocess
# import imageio_ffmpeg as ffmpeg


# def save_video_quality(video_path, output_quality, width, height):
#     # Создайте временный файл для нового видео
#     with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
#         output_path = tmp_file.name
#     print(output_path)
#
#     # Измените качество видео с помощью FFmpeg
#     command = f"ffmpeg -i {video_path} -vf scale={width}:{height} -c:v libx264 -crf 20 -c:a aac -strict experimental {output_path}"
#     os.system(command)
#
#     # Сохраните новое видео как объект File
#     with open(output_path, "rb") as file:
#         django_file = File(file)
#
#     # Создайте запись FormatMovie и сохраните ее в базу данных
#     format_movie = FormatMovie(quality=output_quality, movie_file=django_file)
#     format_movie.save()
#
#     # Удалите временный файл
#     os.remove(output_path)
#
#     return format_movie
#
#
# def save_format_movie(data, movie):
#     video_file = data["movie"]
#     # Получить путь к временному файлу
#     video_path = video_file.temporary_file_path()
#
#     # Измените и сохраните видео в разных качествах
#     save_video_quality(video_path, "720p", 1280, 720)
#     save_video_quality(video_path, "1080p", 1920, 1080)
#
#     # # Создать экземпляр VideoFileClip из временного файла
#     # video_clip = VideoFileClip(video_path)
#     #
#     # # Качество 720p
#     # output_720p = "output_720p.mp4"
#     # video_clip.resize(width=1280).write_videofile(output_720p)
#     #
#     # # Качество 1080p
#     # output_1080p = "output_1080p.mp4"
#     # video_clip.resize(width=1920).write_videofile(output_1080p)
#     #
#     # # Создать записи FormatMovie
#     # with open(output_720p, "rb") as file1, open(output_1080p, "rb") as file2:
#     #     django_file_720 = File(file1)
#     #     django_file_1080 = File(file2)
#     #
#     # with io.BytesIO() as tmp_file_720, io.BytesIO() as tmp_file_1080:
#     #     with open(output_720p, "rb") as file1, open(output_1080p, "rb") as file2:
#     #         tmp_file_720.write(file1.read())
#     #         tmp_file_1080.write(file2.read())
#     #
#     #     # Создайте записи FormatMovie
#     #     FormatMovie.objects.create(movie=movie, quality="720p", movie_file=File(tmp_file_720)).save()
#     #     FormatMovie.objects.create(movie=movie, quality="1080p", movie_file=File(tmp_file_1080)).save()
#     #
#     # # Удалите временные файлы
#     # os.remove(output_720p)
#     # os.remove(output_1080p)


def list_movies(request):
    genre_name = request.query_params.get('genre_name')
    if genre_name:
        movies = Movie.objects.filter(genres__name__icontains=genre_name)
    else:
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
        save_format_movie(serializer.validated_data, movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator
def create_movie(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        movie = serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
