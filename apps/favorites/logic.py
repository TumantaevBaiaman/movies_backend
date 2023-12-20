from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.favorites.models import Favorite
from apps.favorites.serializers import FavoriteSerializer, ViewFavoriteSerializer
from apps.movies.models import Movie
from apps.series.models import Series


def add_favorite(request, content_type, content_id):
    user = request.user
    try:
        favorite = Favorite.objects.get(user=user)
    except Favorite.DoesNotExist:
        favorite = Favorite(user=user)
        favorite.save()

    if content_type == "movie":
        movie = get_object_or_404(Movie, id=content_id)
        favorite.add_to_favorites_movies(movie)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif content_type == "series":
        series = get_object_or_404(Series, id=content_id)
        favorite.add_to_favorites_series(series)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unsupported content type"}, status=status.HTTP_400_BAD_REQUEST)


def remove_favorite(request, content_type, content_id):
    user = request.user
    try:
        favorite = Favorite.objects.get(user=user)
    except Favorite.DoesNotExist:
        favorite = Favorite(user=user)
        favorite.save()

    if content_type == "movie":
        movie = get_object_or_404(Movie, id=content_id)
        favorite.remove_from_favorites_movies(movie)
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif content_type == "series":
        print(content_id)
        series = get_object_or_404(Series, id=content_id)
        favorite.remove_from_favorites_series(series)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "Unsupported content type"}, status=status.HTTP_400_BAD_REQUEST)


def my_favorites(request):
    user = request.user
    try:
        favorite = Favorite.objects.create(user=user).save() if Favorite.objects.filter(user=user).first() is None else Favorite.objects.get(user=user)
        serializer = ViewFavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Favorite.DoesNotExist:
        return Response({"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)
