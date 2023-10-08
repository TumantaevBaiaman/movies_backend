from django.urls import path

from apps.genres import views


urlpatterns = [
    path("create/", views.CreateGenreAPIView.as_view(), name="create-genre"),
    path("list/", views.ListGenreAPIView.as_view(), name="list-genre"),
    path("update_delete/<str:id>/", views.UpdateDestroyGenreAPIView.as_view(), name="update-delete-genre"),
    path("detail/<str:id>/", views.DetailGenreAPIView.as_view(), name="detail-genre")
]