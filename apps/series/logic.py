from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.series.models import Series, Season
from apps.series.serializers import CreateSeriesSerializer, CreateSeasonSerializer, CreateSeriesVideoSerializer, \
    SeriesViewSerializer
from movies_backend.tools import get_filters, paginate_queryset


def create_series(request):
    serializer = CreateSeriesSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as error:
        return Response({"error": error.detail}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_200_OK)


def create_season(request, series_id):
    series = get_object_or_404(Series, id=series_id)

    mutable_data = request.data.copy()

    mutable_data["series"] = series.id

    serializer = CreateSeasonSerializer(data=mutable_data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as error:
        return Response({"error": error.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_series_video(request, content_type, content_id):
    try:
        content_object = None
        if content_type == "series":
            series = get_object_or_404(Series, id=content_id)
            content_object = series
        elif content_type == "season":
            season = get_object_or_404(Season, id=content_id)
            content_object = season
        else:
            return Response({"error": "Invalid content type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateSeriesVideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['content_object'] = content_object
        serializer.validated_data['object_id'] = content_id

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as error:
        return Response({"error": error.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def list_series(request):
    queryset = Series.objects.all()

    filters_data = {
        'title__icontains': request.GET.get('title'),
        'genres__name__in': request.GET.getlist('genres'),
        'is_free': request.GET.get('is_free')
    }
    if request.GET.get('release_date'):
        filters_data['release_date__gte'] = request.GET.get('release_date')
    filters = get_filters(request, filters_data)
    queryset = queryset.filter(**filters)

    paginated_data = paginate_queryset(request, queryset)

    serializer = SeriesViewSerializer(paginated_data['results'], many=True)

    return Response({
        'count': paginated_data['count'],
        'next': paginated_data['next'],
        'previous': paginated_data['previous'],
        'results': serializer.data
    }, status=status.HTTP_200_OK)


def detail_series(request, id):
    series = get_object_or_404(Series, id=id)
    serializer = SeriesViewSerializer(instance=series)
    return Response(serializer.data, status=status.HTTP_200_OK)