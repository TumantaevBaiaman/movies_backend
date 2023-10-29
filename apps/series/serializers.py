from django.contrib.contenttypes.models import ContentType
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
    content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = SeriesVideo
        fields = "__all__"
        extra_kwargs = {
            'object_id': {'required': False},
            'content_type': {'required': False}
        }

    def get_content_type_name(self, obj):
        content_type = ContentType.objects.get_for_model(obj.content_object)
        return content_type.name


class SeriesVideoViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesVideo
        fields = "__all__"


class SeasonViewSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = "__all__"

    def get_videos(self, obj):
        videos = SeriesVideo.objects.filter(object_id=obj.id)
        if videos.first():
            serializer = SeriesVideoViewSerializer(videos, many=True)
            return serializer.data
        else:
            return None


class SeriesViewSerializer(serializers.ModelSerializer):
    seasons = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = "__all__"

    def get_seasons(self, obj):
        seasons = Season.objects.filter(series=obj)
        if seasons.exists():
            serializer = SeasonViewSerializer(seasons, many=True)
            return serializer.data
        else:
            return None

    def get_videos(self, obj):
        videos = SeriesVideo.objects.filter(object_id=obj.id)
        if videos.exists():
            serializer = SeriesVideoViewSerializer(videos, many=True)
            return serializer.data
        else:
            return None




