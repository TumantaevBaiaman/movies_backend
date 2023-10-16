from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.director.models import Director
from apps.director.serializers import DirectorSerializer
from movies_backend.decorators import is_admin_decorator, is_admin_decorator_detail


@is_admin_decorator
def create_director(request):
    serializer = DirectorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator_detail
def delete_director(request, id):  # noqa
    director = get_object_or_404(Director, id=id)
    director.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@is_admin_decorator_detail
def path_director(request, id):    # noqa
    director = get_object_or_404(director, id=id) # noqa
    serializer = DirectorSerializer(director, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator_detail
def put_director(request, id): # noqa
    director = get_object_or_404(Director, id=id) # noqa
    serializer = DirectorSerializer(director, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def detail_director(request, id):
    director = get_object_or_404(Director, id=id)
    serializer = DirectorSerializer(instance=director)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_directors(data):
    directors = Director.objects.all()
    serializer = DirectorSerializer(instance=directors, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
