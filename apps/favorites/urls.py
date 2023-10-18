from django.urls import path

from apps.favorites import views

urlpatterns = [
    path('add/<str:content_type>/<str:content_id>/', views.AddToFavoriteView.as_view(), name='add_to_favorite'),
    path('remove/<str:content_type>/<str:content_id>/', views.RemoveFromFavoriteView.as_view(), name='remove_from_favorite'),
    path('view_favorites/', views.MyFavoritesView.as_view(), name='view_favorites'),
]