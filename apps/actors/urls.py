from django.urls import path
from apps.actors import views

urlpatterns = [
    path("create/", views.CreateActorAPIView.as_view(), name="create-actor"),
    path("list/", views.ListActorAPIView.as_view(), name="list-actor"),
    path("update_delete/<str:id>/", views.UpdateDestroyActorAPIView.as_view(), name="update-delete-actor"),
    path("detail/<str:id>/", views.DetailActorAPIView.as_view(), name="detail-actor")
]