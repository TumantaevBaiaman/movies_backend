from django.urls import path

from apps.series import views

urlpatterns = [
    path('create-series/', views.CreateSeriesView.as_view(), name='create_series'),
    path('create-season/<series_id>/', views.CreateSeasonView.as_view(), name='create_season'),
    path('create-series-video/<content_type>/<content_id>/', views.CreateSeriesVideoView.as_view(), name='create_series_video'),
    path('list/', views.ListSeriesView.as_view(), name="list_series"),
    path('list-moon/', views.ListSeriesMoonView.as_view(), name="list_series-moon"),
    path('detail-series/<id>/', views.DetailSeriesAPIView.as_view(), name="detail_series"),
    path('detail-season/<id>/', views.DetailSeasonAPIView.as_view(), name="detail_season"),
    path('detail-series-video/<id>/', views.DetailSeriesVideoAPIView.as_view(), name="detail_series_video"),
    path('detail-series-video-views/<id>/', views.DetailViewsSeriesVideoAPIView.as_view(), name="detail_series_video"),
]