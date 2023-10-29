from rest_framework import serializers

from apps.favorites.models import Favorite
from apps.movies.serializers import MovieSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class ViewFavoriteSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Favorite
        fields = '__all__'
