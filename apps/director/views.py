from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView

from apps.director.logic import create_director, list_directors, delete_director, put_director, path_director, \
    detail_director
from apps.director.serializers import DirectorSerializer


class CreateDirectorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: DirectorSerializer()},
        request_body=DirectorSerializer(),
        operation_description="""
            `POST` - Добавить режиссер.
            Нужно авторизация и только админ можеть
        """)
    def post(self, request, *args, **kwargs):
        return create_director(request)


class ListDirectorAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        responses={200: DirectorSerializer(many=True)},
        operation_description="""
                `GET` - Получить режиссеры.
                Не нужно авторизация
            """)
    def get(self, request, *args, **kwargs):
        return list_directors(request.data)


class UpdateDestroyDirectorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            204: "No Content - Запрос выполнен успешно."
        },
        operation_description="""
            `DELETE` - Удалить режиссера.
            Нужно авторизация и только админ можеть
    """)
    def delete(self, request, id):  # noqa
        return delete_director(request, id)

    @swagger_auto_schema(
        responses={200: DirectorSerializer()},
        request_body=DirectorSerializer(),
        operation_description="""
            `PUT` - Изменить режиссера.
            Нужно авторизация и только админ можеть
    """)
    def put(self, request, id): # noqa
        return put_director(request, id)

    @swagger_auto_schema(
        responses={200: DirectorSerializer()},
        request_body=DirectorSerializer(),
        operation_description="""
            `PATH` - Изменить режиссера по часьтям.
            Нужно авторизация и только админ можеть
    """)
    def path(self, request, id):    # noqa
        return path_director(request, id)


class DetailDirectorAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: DirectorSerializer()},
        operation_description="""
                `GET` - Получить режиссера по id.
                Не нужно авторизация
        """)
    def get(self, request, id):
        return detail_director(request, id)