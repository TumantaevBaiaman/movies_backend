from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from movies_backend.yasg import urlpatterns as doc_url

v1_api_urls = [
    path("user/", include("apps.users.urls")),
    path("movie/", include("apps.movies.urls")),
    path("genre/", include("apps.genres.urls")),
    path("comment/", include("apps.comments.urls")),
    path("actor/", include("apps.actors.urls")),
    path("director/", include("apps.director.urls")),
    path("favorite/", include("apps.favorites.urls")),
    path("series/", include("apps.series.urls")),
]

api_urls = [
    path("v1/", include((v1_api_urls, "v1"), namespace="v1")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include((api_urls, ""))),
]

urlpatterns += doc_url

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
