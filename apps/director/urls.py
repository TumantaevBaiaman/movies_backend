from django.urls import path

from apps.director import views

urlpatterns = [
    path("create/", views.CreateDirectorAPIView.as_view(), name="create-director"),
    path("list/", views.ListDirectorAPIView.as_view(), name="list-director"),
    path("update_delete/<str:id>/", views.UpdateDestroyDirectorAPIView.as_view(), name="update-delete-director"),
    path("detail/<str:id>/", views.DetailDirectorAPIView.as_view(), name="detail-director")
]