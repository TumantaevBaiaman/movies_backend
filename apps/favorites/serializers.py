from rest_framework import serializers

from apps.favorites.models import Favorite
from apps.movies.serializers import MovieSerializer, MovieViewSerializer
from apps.series.serializers import SeriesVideoViewSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class ViewFavoriteSerializer(serializers.ModelSerializer):
    movies = MovieViewSerializer(many=True, required=False)
    series = SeriesVideoViewSerializer(many=True, required=False)

    class Meta:
        model = Favorite
        fields = '__all__'
