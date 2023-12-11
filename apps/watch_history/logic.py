from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from apps.movies.models import Movie
from apps.series.models import Series, SeriesVideo
from apps.watch_history.models import WatchHistory
from apps.watch_history.serializers import WatchHistorySerializer
from movies_backend.tools import paginate_queryset


def add_to_watch_history(request, content_type, content_id):
    user = request.user
    if user.is_authenticated:
        if content_type == 'movie':
            movie = get_object_or_404(Movie, pk=content_id)
            history_entry, created = WatchHistory.objects.get_or_create(user=user, movie=movie)
        elif content_type == 'series':
            series = get_object_or_404(SeriesVideo, pk=content_id)
            history_entry, created = WatchHistory.objects.get_or_create(user=user, series=series)
        else:
            return JsonResponse({'error': 'Invalid content type'})

        # Если запись уже существует, обновим timestamp
        if not created:
            history_entry.timestamp = timezone.now()
            history_entry.save()

        return JsonResponse({'success': 'Added to watch history'})
    else:
        return JsonResponse({'error': 'User not authenticated'})


def watch_history(request):
    user = request.user
    history = WatchHistory.objects.filter(user=user)
    paginated_data = paginate_queryset(request, history)
    serializer = WatchHistorySerializer(paginated_data['results'], many=True)
    return Response({
        'count': paginated_data['count'],
        'next': paginated_data['next'],
        'previous': paginated_data['previous'],
        'results': serializer.data
    }, status=status.HTTP_200_OK)