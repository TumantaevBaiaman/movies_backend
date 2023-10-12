from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from apps.genres.logic import create_genre, list_genres, delete_genre, put_genre, path_genre, detail_genre
from apps.genres.serializers import GenreSerializer


class CreateGenreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: GenreSerializer()},
        request_body=GenreSerializer(),
        operation_description="""
            `POST` - Добавить жанр.
            Нужно авторизация и только админ можеть
        """)
    def post(self, request, *args, **kwargs):
        return create_genre(request)


class ListGenreAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        responses={200: GenreSerializer(many=True)},
        operation_description="""
                `GET` - Получить жанры.
                Не нужно авторизация
            """)
    def get(self, request, *args, **kwargs):
        return list_genres(request.data)


class UpdateDestroyGenreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            204: "No Content - Запрос выполнен успешно."
        },
        operation_description="""
            `DELETE` - Удалить жанр.
            Нужно авторизация и только админ можеть
    """)
    def delete(self, request, id):  # noqa
        return delete_genre(request, id)

    @swagger_auto_schema(
        responses={200: GenreSerializer()},
        request_body=GenreSerializer(),
        operation_description="""
            `PUT` - Изменить жанр.
            Нужно авторизация и только админ можеть
    """)
    def put(self, request, id): # noqa
        return put_genre(request, id)

    @swagger_auto_schema(
        responses={200: GenreSerializer()},
        request_body=GenreSerializer(),
        operation_description="""
            `PATH` - Изменить жанр по часьтям.
            Нужно авторизация и только админ можеть
    """)
    def path(self, request, id):    # noqa
        return path_genre(request, id)


class DetailGenreAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: GenreSerializer()},
        operation_description="""
                `GET` - Получить жанр по id.
                Не нужно авторизация
        """)
    def get(self, request, id):
        return detail_genre(request, id)

