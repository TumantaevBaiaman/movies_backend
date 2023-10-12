from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.movies.models import Movie
from apps.movies.serializers import MovieSerializer
from movies_backend.decorators import is_admin_decorator_detail, is_admin_decorator


def list_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(instance=movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def detail_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    serializer = MovieSerializer(instance=movie)
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
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)