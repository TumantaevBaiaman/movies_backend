from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from apps.genres.logic import create_genre, list_genres, delete_genre, put_genre, path_genre, detail_genre


class CreateGenreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return create_genre(request)


class ListGenreAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return list_genres(request.data)


class UpdateDestroyGenreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):  # noqa
        return delete_genre(request, id)

    def put(self, request, id): # noqa
        return put_genre(request, id)

    def path(self, request, id):    # noqa
        return path_genre(request, id)


class DetailGenreAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        return detail_genre(request, id)

