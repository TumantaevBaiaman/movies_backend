import io
import os
import tempfile
from datetime import datetime

import boto3

from django.core.files import File
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.genres.models import Genre
from apps.movies.models import Movie, FormatMovie
from apps.movies.serializers import MovieSerializer, FormatMovieSerializer, MovieViewSerializer
from movies_backend import settings
from movies_backend.decorators import is_admin_decorator_detail, is_admin_decorator
from movies_backend.tools import get_filters, paginate_queryset

from moviepy.editor import VideoFileClip


def split_video_quality(input_path, output_path_360p, output_path_720p, output_path_1080p):
    video_clip = VideoFileClip(input_path)

    # Создайте копии видео с разным качеством
    video_360p = video_clip.resize(height=360)
    video_720p = video_clip.resize(height=720)
    video_1080p = video_clip.resize(height=1080)

    # Сохраните видео в различных качествах
    video_360p.write_videofile(output_path_360p, codec='libx264', audio_codec='aac')
    video_720p.write_videofile(output_path_720p, codec='libx264', audio_codec='aac')
    video_1080p.write_videofile(output_path_1080p, codec='libx264', audio_codec='aac')

    # Освободите ресурсы
    video_clip.close()
    video_360p.close()
    video_720p.close()
    video_1080p.close()


def list_movies(request):
    queryset = Movie.objects.all()
    filters_data = {
        'title__icontains': request.GET.get('title'),
        'genres__name__in': request.GET.getlist('genres'),
        'is_free': request.GET.get('is_free')
    }
    if request.GET.get('release_date'):
        filters_data['release_date__gte'] = request.GET.get('release_date')
    filters = get_filters(request, filters_data)
    queryset = queryset.filter(**filters)
    paginated_data = paginate_queryset(request, queryset)

    serializer = MovieViewSerializer(paginated_data['results'], many=True)
    return Response({
        'count': paginated_data['count'],
        'next': paginated_data['next'],
        'previous': paginated_data['previous'],
        'results': serializer.data
    }, status=status.HTTP_200_OK)


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
        # save_format_movie(serializer.validated_data, movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator
def create_movie(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        movie = serializer.save()
        # video_clip = VideoFileClip(movie.movie.url)
        #
        # elastic_transcoder = boto3.client('elastictranscoder', region_name=settings.AWS_S3_REGION_NAME)


        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
