from django.urls import path
from apps.watch_history import views

urlpatterns = [
    path("list/", views.WatchHistoryAPIView.as_view(), name="watch_history")
]