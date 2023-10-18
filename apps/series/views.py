from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from apps.series.logic import create_series, create_season
from movies_backend.permissions import IsAuthenticatedAdmin


class CreateSeriesView(APIView):
    permission_classes = [IsAuthenticatedAdmin]

    def post(self, request, content_type, content_id):
        return create_series(request, content_type, content_id)


class CreateSeasonView(APIView):
    permission_classes = [IsAuthenticatedAdmin]

    def post(self, request, series_id):
        return create_season(request, series_id)
