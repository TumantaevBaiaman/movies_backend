from rest_framework import serializers

from apps.series.models import Series, Season, SeriesVideo


class CreateSeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = "__all__"


class CreateSeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = "__all__"


class CreateSeriesVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = "__all__"



