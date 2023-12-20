from django.urls import path
from apps.users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("register/", views.UserRegistrationAPIView.as_view(), name="register"),
    path("confirm_code_register/", views.ConfirmCodeRegisterAPIView.as_view(), name="confirm_code_register"),
    path("resend_confirm_code_register/", views.ResendConfirmCodeRegisterAPIView.as_view(), name="resend_confirm_code_register"),
    path("reset_password/", views.SendResetCodeAPIView.as_view(), name="reset"),
    path("reset_verity_code/", views.VerifyResetCodeAPIView.as_view(), name="reset_verify_code"),
    path('reset_change_password/', views.ResetChangePasswordAPIView.as_view(), name='reset_change_password'),
    path('login/', views.UserLoginAPIView.as_view(), name='token_obtain_pair'),
    path('profile/', views.UserProfileAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('subscription/', views.SubscriptionAPIView.as_view(), name='subscription'),
    path('notification_list/', views.NotificationListAPIView.as_view(), name="notification_list"),
    path('notification_detail/<int:id>/', views.NotificationDetailAPIView.as_view(), name="notification_detail")
]
