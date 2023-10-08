from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.genres.models import Genre
from apps.genres.serializers import GenreSerializer
from movies_backend.decorators import is_admin_decorator, is_admin_decorator_detail


@is_admin_decorator
def create_genre(request):
    serializer = GenreSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


@is_admin_decorator_detail
def delete_genre(request, id):  # noqa
    genre = get_object_or_404(Genre, id=id)
    genre.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@is_admin_decorator_detail
def path_genre(request, id):    # noqa
    genre = get_object_or_404(Genre, id=id) # noqa
    serializer = GenreSerializer(genre, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator_detail
def put_genre(request, id): # noqa
    genre = get_object_or_404(Genre, id=id) # noqa
    serializer = GenreSerializer(genre, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def detail_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    serializer = GenreSerializer(instance=genre)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_genres(data):
    genres = Genre.objects.all()
    serializer = GenreSerializer(instance=genres, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
