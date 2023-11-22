from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView

from apps.comments.logic import create_comment, list_comments, path_comment, put_comment, delete_comment, \
    detail_comment, create_comment_series, detail_comment_series, delete_comment_series, put_comment_series, \
    path_comment_series, list_comments_series
from apps.comments.serializers import CommentSerializer, CommentSeriesSerializer


class CreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CommentSerializer()},
        request_body=CommentSerializer(),
        operation_description="""
            `POST` - Добавить комментарии.
            Нужно авторизация
        """)
    def post(self, request, id_movie, *args, **kwargs):
        return create_comment(request, id_movie)


class ListCommentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        responses={200: CommentSerializer(many=True)},
        operation_description="""
                `GET` - Получить комментрии.
                Не нужно авторизация
            """)
    def get(self, request, id_movie, *args, **kwargs):
        return list_comments(request, id_movie)


class UpdateDestroyCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            204: "No Content - Запрос выполнен успешно."
        },
        operation_description="""
            `DELETE` - Удалить комментарии.
            Нужно авторизация и только админ или создател комментарии можеть
    """)
    def delete(self, request, id):  # noqa
        return delete_comment(request, id)

    @swagger_auto_schema(
        responses={200: CommentSerializer()},
        request_body=CommentSerializer(),
        operation_description="""
            `PUT` - Изменить комментарии.
            Нужно авторизация и только админ или создатель комментарии можеть
    """)
    def put(self, request, id): # noqa
        return put_comment(request, id)

    @swagger_auto_schema(
        responses={200: CommentSerializer()},
        request_body=CommentSerializer(),
        operation_description="""
            `PATH` - Изменить комментарии по часьтям.
            Нужно авторизация и только админ или создатель комментарии можеть
    """)
    def path(self, request, id):    # noqa
        return path_comment(request, id)


class DetailCommentAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: CommentSerializer()},
        operation_description="""
                `GET` - Получить комментарии по id.
                Не нужно авторизация
        """)
    def get(self, request, id):
        return detail_comment(request, id)


# series
class CreateCommentSeriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: CommentSeriesSerializer()},
        request_body=CommentSeriesSerializer(),
        operation_description="""
            `POST` - Добавить комментарии.
            Нужно авторизация
        """)
    def post(self, request, id_series, *args, **kwargs):
        return create_comment_series(request, id_series)


class DetailCommentSeriesAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: CommentSerializer()},
        operation_description="""
                `GET` - Получить комментарии по id.
                Не нужно авторизация
        """)
    def get(self, request, id):
        return detail_comment_series(request, id)


class UpdateDestroyCommentSeriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            204: "No Content - Запрос выполнен успешно."
        },
        operation_description="""
            `DELETE` - Удалить комментарии.
            Нужно авторизация и только админ или создател комментарии можеть
    """)
    def delete(self, request, id):  # noqa
        return delete_comment_series(request, id)

    @swagger_auto_schema(
        responses={200: CommentSerializer()},
        request_body=CommentSerializer(),
        operation_description="""
            `PUT` - Изменить комментарии.
            Нужно авторизация и только админ или создатель комментарии можеть
    """)
    def put(self, request, id): # noqa
        return put_comment_series(request, id)

    @swagger_auto_schema(
        responses={200: CommentSerializer()},
        request_body=CommentSerializer(),
        operation_description="""
            `PATH` - Изменить комментарии по часьтям.
            Нужно авторизация и только админ или создатель комментарии можеть
    """)
    def path(self, request, id):    # noqa
        return path_comment_series(request, id)


class ListCommentSeriesAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        responses={200: CommentSerializer(many=True)},
        operation_description="""
                `GET` - Получить комментрии.
                Не нужно авторизация
            """)
    def get(self, request, id_series, *args, **kwargs):
        return list_comments_series(request, id_series)
