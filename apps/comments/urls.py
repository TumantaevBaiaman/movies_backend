from django.urls import path
from apps.comments import views

urlpatterns = [
    path("create/<str:id_movie>/", views.CreateCommentAPIView.as_view(), name="create-comment"),
    path("list/", views.ListCommentAPIView.as_view(), name="list-comments"),
    path("update_delete/<str:id>/", views.UpdateDestroyCommentAPIView.as_view(), name="update-delete-comment"),
    path("detail/<str:id>/", views.DetailCommentAPIView.as_view(), name="detail-comment")
]