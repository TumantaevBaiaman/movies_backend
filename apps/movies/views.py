from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.movies.logic import list_movies, detail_movie, delete_movie, put_movie, path_movie, create_movie
from apps.movies.serializers import MovieSerializer


class CreateMovieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: MovieSerializer()},
        request_body=MovieSerializer(),
        operation_description="""
            `POST` - Добавить фильм.
            Нужно авторизация и только админ можеть
        """)
    def post(self, request, *args, **kwargs):
        return create_movie(request)


class ListMovieAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: MovieSerializer(many=True)},
        operation_description="""
                    `GET` - Получить фильмы.
                    Не нужно авторизация
                """)
    def get(self, request):
        return list_movies(request)


class DetailMovieAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: MovieSerializer()},
        operation_description="""
                `GET` - Получить фильм по id.
                Не нужно авторизация
        """)
    def get(self, request, id):
        return detail_movie(request, id)


class UpdateDestroyMovieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            204: "No Content - Запрос выполнен успешно."
        },
        operation_description="""
            `DELETE` - Удалить фильм.
            Нужно авторизация и только админ можеть
    """)
    def delete(self, request, id):  # noqa
        return delete_movie(request, id)

    @swagger_auto_schema(
        responses={200: MovieSerializer()},
        request_body=MovieSerializer(),
        operation_description="""
            `PUT` - Изменить фильм.
            Нужно авторизация и только админ можеть
    """)
    def put(self, request, id): # noqa
        return put_movie(request, id)

    @swagger_auto_schema(
        responses={200: MovieSerializer()},
        request_body=MovieSerializer(),
        operation_description="""
            `PATH` - Изменить фильм по часьтям.
            Нужно авторизация и только админ можеть
    """)
    def path(self, request, id):    # noqa
        return path_movie(request, id)