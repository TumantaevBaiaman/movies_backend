from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from apps.actors.logic import create_actor, list_actors, delete_actor, put_actor, path_actor, detail_actor
from apps.actors.serializers import ActorSerializer


class CreateActorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ActorSerializer()},
        request_body=ActorSerializer(),
        operation_description="""
            `POST` - Добавить жанр.
            Нужно авторизация и только админ можеть
        """)
    def post(self, request, *args, **kwargs):
        return create_actor(request)


class ListActorAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        responses={200: ActorSerializer(many=True)},
        operation_description="""
                `GET` - Получить жанры.
                Не нужно авторизация
            """)
    def get(self, request, *args, **kwargs):
        return list_actors(request.data)


class UpdateDestroyActorAPIView(APIView):
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
        return delete_actor(request, id)

    @swagger_auto_schema(
        responses={200: ActorSerializer()},
        request_body=ActorSerializer(),
        operation_description="""
            `PUT` - Изменить жанр.
            Нужно авторизация и только админ можеть
    """)
    def put(self, request, id): # noqa
        return put_actor(request, id)

    @swagger_auto_schema(
        responses={200: ActorSerializer()},
        request_body=ActorSerializer(),
        operation_description="""
            `PATH` - Изменить актера по часьтям.
            Нужно авторизация и только админ можеть
    """)
    def path(self, request, id):    # noqa
        return path_actor(request, id)


class DetailActorAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: ActorSerializer()},
        operation_description="""
                `GET` - Получить актер по id.
                Не нужно авторизация
        """)
    def get(self, request, id):
        return detail_actor(request, id)

