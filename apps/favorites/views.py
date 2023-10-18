from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.favorites.logic import add_favorite, remove_favorite, my_favorites


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "Запрос выполнен успешно."
        },
        operation_description="""
                `POST` - добавить в избранных
        """)
    def post(self, request, content_type, content_id, *args, **kwargs):
        return add_favorite(request, content_type, content_id)


class RemoveFromFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "Запрос выполнен успешно."
        },
        operation_description="""
                    `POST` - убрать из избранных
            """)
    def post(self, request, content_type, content_id, *args, **kwargs):
        return remove_favorite(request, content_type, content_id)


class MyFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "Запрос выполнен успешно."
        },
        operation_description="""
                `GET` - посмотреть избрвнных. 
        """)
    def get(self, request, *args, **kwargs):
        return my_favorites(request)
