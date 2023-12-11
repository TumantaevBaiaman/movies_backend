from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from rest_framework import serializers

from apps.comments.models import CommentSeries
from apps.comments.serializers import CommentSeriesSerializer
from apps.favorites.models import Favorite
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
    rating = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = SeriesVideo
        fields = "__all__"

    def get_rating(self, obj):
        comments = CommentSeries.objects.filter(series=obj)
        if comments.exists():
            total_rating = comments.aggregate(avg_rating=Avg('rating'))
            return total_rating['avg_rating']
        else:
            return None

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                favorite = Favorite.objects.get(user=request.user)
                return obj in favorite.series.all()
            except Favorite.DoesNotExist:
                pass
        return False


class SeasonViewSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()

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

    def get_total_rating(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        videos = SeriesVideo.objects.filter(content_type=content_type, object_id=obj.id)
        comments = CommentSeries.objects.filter(series__in=videos)

        if comments.exists():
            total_rating = comments.aggregate(avg_rating=Avg('rating'))
            return total_rating['avg_rating']
        else:
            return None


class SeriesViewSerializer(serializers.ModelSerializer):
    seasons = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()

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

    def get_total_rating(self, obj):
        content_type_series = ContentType.objects.get_for_model(obj)
        series_videos = SeriesVideo.objects.filter(content_type=content_type_series, object_id=obj.id)
        comments_series_videos = CommentSeries.objects.filter(series__in=series_videos)

        if comments_series_videos.exists():
            total_rating_series_videos = comments_series_videos.aggregate(avg_rating=Avg('rating'))
            avg_rating_series_videos = total_rating_series_videos['avg_rating']
        else:
            avg_rating_series_videos = None

        # Calculate total rating for the series across all seasons
        seasons = Season.objects.filter(series=obj)
        total_ratings_seasons = 0
        total_seasons = 0

        for season in seasons:
            content_type_season = ContentType.objects.get_for_model(season)
            season_videos = SeriesVideo.objects.filter(content_type=content_type_season, object_id=season.id)
            comments_season_videos = CommentSeries.objects.filter(series__in=season_videos)

            if comments_season_videos.exists():
                total_rating_season = comments_season_videos.aggregate(avg_rating=Avg('rating'))
                avg_rating_season = total_rating_season['avg_rating']
                total_ratings_seasons += avg_rating_season
                total_seasons += 1

        if total_seasons > 0:
            avg_rating_seasons = total_ratings_seasons / total_seasons
        else:
            avg_rating_seasons = None

        # Calculating the overall rating for the series
        if avg_rating_series_videos and avg_rating_seasons:
            overall_rating = (avg_rating_series_videos + avg_rating_seasons) / 2
        elif avg_rating_series_videos:
            overall_rating = avg_rating_series_videos
        else:
            overall_rating = avg_rating_seasons

        return {
            "series_total_rating": overall_rating,
            "series_videos_rating": avg_rating_series_videos,
            "seasons_avg_rating": avg_rating_seasons
        }
