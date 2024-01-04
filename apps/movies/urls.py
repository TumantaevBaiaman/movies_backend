from django.urls import path
from apps.movies import views

urlpatterns = [
    path("create/", views.CreateMovieAPIView.as_view(), name="create-movie"),
    path("list", views.ListMovieAPIView.as_view(), name="list-movie"),
    path("list-moon/", views.ListMovieMoonAPIView.as_view(), name="list-movie-moon"),
    path("update_delete/<str:id>/", views.UpdateDestroyMovieAPIView.as_view(), name="update-delete-movie"),
    path("detail/<str:id>/", views.DetailMovieAPIView.as_view(), name="detail-movie"),
    path("detail-views/<str:id>/", views.DetailViewsMovieAPIView.as_view(), name="detail-movie-views"),
    path("list-genre/<str:id_genre>/", views.ListMovieGenreAPIView.as_view(), name="list-genre-movie"),
    path("list-recommendation/<str:id_genre>/", views.ListMovieRecommendationAPIView.as_view(), name="list-recommendation-movie"),
    path("top-list/", views.ListMovieTopAPIView.as_view(), name="list-top-movie")
]