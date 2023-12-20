from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.comments.models import Comment, CommentSeries
from apps.comments.serializers import CommentSerializer, CommentSeriesSerializer
from apps.movies.models import Movie
from apps.series.models import Series
from movies_backend.tools import paginate_queryset


def create_comment(request, id_movie):
    user = request.user
    movie = get_object_or_404(Movie, id=id_movie)
    request.data['movie'] = movie.id
    request.data['user'] = user.id
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_comment(request, id):  # noqa
    user = request.user
    comment = get_object_or_404(Comment, id=id)
    if comment.user == user or user.is_admin:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            {"error": "Доступ запрещен так как это не ваш комментарии"},
            status=status.HTTP_403_FORBIDDEN
        )


def path_comment(request, id):    # noqa
    user = request.user
    comment = get_object_or_404(Comment, id=id) # noqa
    if comment.user == user or user.is_admin:
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"error": "Доступ запрещен так как это не ваш комментарии"},
            status=status.HTTP_403_FORBIDDEN
        )


def put_comment(request, id): # noqa
    user = request.user
    comment = get_object_or_404(Comment, id=id) # noqa
    if comment.user == user or user.is_admin:
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"error": "Доступ запрещен так как это не ваш комментарии"},
            status=status.HTTP_403_FORBIDDEN
        )


def detail_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    serializer = CommentSerializer(instance=comment)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_comments(request, id_movie):
    comments = Comment.objects.filter(movie_id=id_movie)
    paginated_data = paginate_queryset(request, comments)
    serializer = CommentSerializer(paginated_data['results'], many=True)
    return Response({
        'count': paginated_data['count'],
        'next': paginated_data['next'],
        'previous': paginated_data['previous'],
        'results': serializer.data
    }, status=status.HTTP_200_OK)


# series
def create_comment_series(request, id_series):
    user = request.user
    series = get_object_or_404(Series, id=id_series)
    mutable_data = request.data.copy()
    mutable_data['series'] = series.id
    mutable_data['user'] = user.id
    serializer = CommentSeriesSerializer(data=mutable_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_comment_series(request, id):  # noqa
    user = request.user
    comment = get_object_or_404(CommentSeries, id=id)
    if comment.user == user or user.is_admin:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            {"error": "Доступ запрещен так как это не ваш комментарии"},
            status=status.HTTP_403_FORBIDDEN
        )


def path_comment_series(request, id):    # noqa
    user = request.user
    comment = get_object_or_404(CommentSeries, id=id) # noqa
    if comment.user == user or user.is_admin:
        serializer = CommentSeriesSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"error": "Доступ запрещен так как это не ваш комментарии"},
            status=status.HTTP_403_FORBIDDEN
        )


def put_comment_series(request, id): # noqa
    user = request.user
    comment = get_object_or_404(CommentSeries, id=id) # noqa
    if comment.user == user or user.is_admin:
        serializer = CommentSeriesSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"error": "Доступ запрещен так как это не ваш комментарии"},
            status=status.HTTP_403_FORBIDDEN
        )


def detail_comment_series(request, id):
    comment = get_object_or_404(CommentSeries, id=id)
    serializer = CommentSeriesSerializer(instance=comment)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_comments_series(request, id_series):
    comments = CommentSeries.objects.filter(series_id=id_series)
    paginated_data = paginate_queryset(request, comments)
    serializer = CommentSeriesSerializer(paginated_data['results'], many=True)
    return Response({
        'count': paginated_data['count'],
        'next': paginated_data['next'],
        'previous': paginated_data['previous'],
        'results': serializer.data
    }, status=status.HTTP_200_OK)