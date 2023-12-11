from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from apps.watch_history.logic import watch_history


class WatchHistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
                            `GET` - История.
                            """
    )
    def get(self, request, *args, **kwargs):
        return watch_history(request)
