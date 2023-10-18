from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.series.models import Series, Season
from apps.series.serializers import CreateSeriesSerializer, CreateSeasonSerializer, CreateSeriesVideoSerializer
from movies_backend.decorators import is_admin_decorator


@is_admin_decorator
def create_series(request):

    serializer = CreateSeriesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


def create_season(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    request.data["series"] = series
    serializer = CreateSeasonSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


def create_series_video(request, content_type, content_id):
    if content_type == "series":
        series = get_object_or_404(Series, id=content_id)
        request.data["content_object"] = series
    elif content_type == "season":
        season = get_object_or_404(Season, id=content_id)
        request.data["content_object"] = season
    serializer = CreateSeriesVideoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.validated_data, status=status.HTTP_200_OK)
