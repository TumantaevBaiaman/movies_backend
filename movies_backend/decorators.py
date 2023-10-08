from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from apps.users.models import User


"""
декоратор для проверки админа
"""
def is_admin_decorator(func):   # noqa

    @wraps(func)
    def wrapper(request):
        try:
            user = request.user
        except AttributeError as e:
            return Response(e, status=status.HTTP_401_UNAUTHORIZED)

        current_user = User.objects.get(id=user.id)
        if current_user.is_admin:  # noqa
            return func(request)
        return Response(
            {"error": "Доступ запрещен"},
            status=status.HTTP_403_FORBIDDEN
        )

    return wrapper


def is_admin_decorator_detail(func):   # noqa

    @wraps(func)
    def wrapper(request, id):
        try:
            user = request.user
        except AttributeError as e:
            return Response(e, status=status.HTTP_401_UNAUTHORIZED)

        current_user = User.objects.get(id=user.id)
        if current_user.is_admin:  # noqa
            return func(request, id)
        return Response(
            {"error": "Доступ запрещен"},
            status=status.HTTP_403_FORBIDDEN
        )

    return wrapper
