from rest_framework import serializers

from apps.comments.models import Comment, CommentSeries


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentSeries
        fields = "__all__"
