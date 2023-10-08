from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.users.logic import create_user_with_tokens, profile_user, confirm_code_register, resend_confirm_code_register, \
    reset_code, verify_reset_code, reset_change_password, login_user


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):   # noqa
        return create_user_with_tokens(request)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):   # noqa
        return login_user(request)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):   # noqa
        return profile_user(request.user)


class ConfirmCodeRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return confirm_code_register(request)


class ResendConfirmCodeRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return resend_confirm_code_register(request)


class SendResetCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return reset_code(request)


class VerifyResetCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        return verify_reset_code(request, token)


class ResetChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return reset_change_password(request)



