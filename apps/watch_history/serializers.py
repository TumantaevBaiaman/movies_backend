from rest_framework import serializers

from apps.movies.serializers import MovieViewSerializer
from apps.series.serializers import SeriesVideoViewSerializer
from apps.watch_history.models import WatchHistory


class WatchHistorySerializer(serializers.ModelSerializer):
    movie = MovieViewSerializer()
    series = SeriesVideoViewSerializer()

    class Meta:
        model = WatchHistory
        fields = "__all__"
