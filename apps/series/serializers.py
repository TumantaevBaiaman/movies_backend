from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from rest_framework import serializers

from apps.actors.serializers import ActorSerializer
from apps.comments.models import CommentSeries, Comment
from apps.comments.serializers import CommentSeriesSerializer
from apps.director.serializers import DirectorSerializer
from apps.favorites.models import Favorite
from apps.genres.serializers import GenreSerializer
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
    genres = GenreSerializer(many=True, required=False)
    actors = ActorSerializer(many=True, required=False)
    directors = DirectorSerializer(many=True, required=False)
    seasons = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

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

    def get_rating(self, obj):
        comments = CommentSeries.objects.filter(series=obj)
        if comments.exists():
            rating = round(sum([int(i.rating) for i in comments]) / len(comments), 1)
            return rating
        else:
            return 5.0

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                favorite = Favorite.objects.get(user=request.user)
                return obj in favorite.series.all()
            except Favorite.DoesNotExist:
                pass
        return False
