from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.series.logic import create_series, create_season, create_series_video, list_series
from apps.series.serializers import CreateSeriesSerializer, CreateSeasonSerializer
from movies_backend.permissions import IsAuthenticatedAdmin


class CreateSeriesView(APIView):
    permission_classes = [IsAuthenticatedAdmin]

    @swagger_auto_schema(
        responses={200: CreateSeriesSerializer()},
        request_body=CreateSeriesSerializer(),
        operation_description="""
                `POST` - Создать сериал.
                Нужно авторизация и только админ можеть
        """)
    def post(self, request):
        return create_series(request)


class CreateSeasonView(APIView):
    permission_classes = [IsAuthenticatedAdmin]

    @swagger_auto_schema(
        responses={200: CreateSeasonSerializer()},
        request_body=CreateSeasonSerializer(),
        operation_description="""
                    `POST` - Создать сезон сериала.
                    Нужно авторизация и только админ можеть
            """)
    def post(self, request, series_id):
        return create_season(request, series_id)


class CreateSeriesVideoView(APIView):
    permission_classes = [IsAuthenticatedAdmin]

    @swagger_auto_schema(
        responses={200: CreateSeriesSerializer()},
        request_body=CreateSeriesSerializer(),
        operation_description="""
                `POST` - Добавить видео на сериал или на сезон.
                content_type - если добавить только на сериал укажите series, если добавите на какой то сезон укажите season
                content_id - укажите id сериала
                Нужно авторизация и только админ можеть
        """)
    def post(self, request, content_type, content_id):
        return create_series_video(request, content_type, content_id)


class ListSeriesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return list_series(request)


