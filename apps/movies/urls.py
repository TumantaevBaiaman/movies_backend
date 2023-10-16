from django.urls import path
from apps.movies import views

urlpatterns = [
    path("create/", views.CreateMovieAPIView.as_view(), name="create-movie"),
    path("list/", views.ListMovieAPIView.as_view(), name="list-movie"),
    path("update_delete/<str:id>/", views.UpdateDestroyMovieAPIView.as_view(), name="update-delete-movie"),
    path("detail/<str:id>/", views.DetailMovieAPIView.as_view(), name="detail-movie"),
    path("list-genre/<str:id_genre>/", views.ListMovieGenreAPIView.as_view(), name="list-genre-movie"),
    path("list-recommendation/<str:id_genre>/", views.ListMovieRecommendationAPIView.as_view(), name="list-recommendation-movie")
]