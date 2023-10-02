from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from movies_backend.yasg import urlpatterns as doc_url

v1_api_urls = [
    path("user/", include("apps.users.urls")),
]

api_urls = [
    path("v1/", include((v1_api_urls, "v1"), namespace="v1")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include((api_urls, ""))),
]

urlpatterns += doc_url

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
