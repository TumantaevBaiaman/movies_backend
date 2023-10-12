from django.urls import path
from apps.movies import views

urlpatterns = [
    path("create/", views.CreateMovieAPIView.as_view(), name="create-genre"),
    path("list/", views.ListMovieAPIView.as_view(), name="list-genre"),
    path("update_delete/<str:id>/", views.UpdateDestroyMovieAPIView.as_view(), name="update-delete-genre"),
    path("detail/<str:id>/", views.DetailMovieAPIView.as_view(), name="detail-genre")
]