from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from apps.actors.serializers import ActorSerializer
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.director.serializers import DirectorSerializer
from apps.genres.serializers import GenreSerializer
from apps.movies.models import Movie, FormatMovie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class MovieViewSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)
    actors = ActorSerializer(many=True, required=False)
    directors = DirectorSerializer(many=True, required=False)
    comments = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_comments(self, obj):  # noqa
        comments = Comment.objects.filter(movie=obj)
        if comments.exists():
            serializer = CommentSerializer(comments, many=True)
            return serializer.data
        else:
            return None

    def get_rating(self, obj):  # noqa
        comments = Comment.objects.filter(movie=obj)
        if comments.exists():
            rating = round(sum([int(i.rating) for i in comments])/len(comments), 1)
            return rating
        else:
            return 5.0


class FormatMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormatMovie
        fields = "__all__"


