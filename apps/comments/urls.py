from django.urls import path, include
from apps.comments import views

series_urls = [
    path("create/<str:id_series>/", views.CreateCommentSeriesAPIView.as_view(), name="create-comment-series"),
    path("list/<str:id_series>/", views.ListCommentSeriesAPIView.as_view(), name="list-comments-series"),
    path("update_delete/<str:id>/", views.UpdateDestroyCommentSeriesAPIView.as_view(),
         name="update-delete-comment-series"),
    path("detail/<str:id>/", views.DetailCommentSeriesAPIView.as_view(), name="detail-comment-series")
]

movies_urls = [
    path("create/<str:id_movie>/", views.CreateCommentAPIView.as_view(), name="create-comment"),
    path("list/<str:id_movie>/", views.ListCommentAPIView.as_view(), name="list-comments"),
    path("update_delete/<str:id>/", views.UpdateDestroyCommentAPIView.as_view(), name="update-delete-comment"),
    path("detail/<str:id>/", views.DetailCommentAPIView.as_view(), name="detail-comment"),
]

urlpatterns = [
    path("series/", include((series_urls, ""))),
    path("movies/", include((movies_urls, "")))
]