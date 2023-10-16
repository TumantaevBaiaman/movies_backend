from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.actors.models import Actor
from apps.actors.serializers import ActorSerializer
from movies_backend.decorators import is_admin_decorator, is_admin_decorator_detail


@is_admin_decorator
def create_actor(request):
    serializer = ActorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator_detail
def delete_actor(request, id):  # noqa
    actor = get_object_or_404(Actor, id=id)
    actor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@is_admin_decorator_detail
def path_actor(request, id):    # noqa
    actor = get_object_or_404(actor, id=id) # noqa
    serializer = ActorSerializer(actor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@is_admin_decorator_detail
def put_actor(request, id): # noqa
    actor = get_object_or_404(Actor, id=id) # noqa
    serializer = ActorSerializer(actor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def detail_actor(request, id):
    actor = get_object_or_404(Actor, id=id)
    serializer = ActorSerializer(instance=actor)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_actors(data):
    actors = Actor.objects.all()
    serializer = ActorSerializer(instance=actors, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
