from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.logic import create_user_with_tokens, profile_user, confirm_code_register, resend_confirm_code_register, \
    reset_code, verify_reset_code, reset_change_password, login_user, subscription, subscription_detail
from apps.users.serializers import LoginUserSerializer, UserRegisterSerializer, UserSerializer, \
    ConfirmCodeRegisterSerializer, SubscriptionSerializer


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: UserRegisterSerializer()},
        request_body=UserRegisterSerializer(),
        operation_description="""
                `POST` - Регистрация пользователя.
                После регистрации на почту придет почта
                Не требуется авторизация.
                """
    )
    def post(self, request, *args, **kwargs):   # noqa
        return create_user_with_tokens(request)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: LoginUserSerializer()},
        request_body=LoginUserSerializer(),
        operation_description="""
            `POST` - Авторизация пользователя.
            Не требуется авторизация.
            """
    )
    def post(self, request, *args, **kwargs):   # noqa
        return login_user(request)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        operation_description="""
                `GET` - Профил пользователя.
                """
    )
    def get(self, request, *args, **kwargs):   # noqa
        return profile_user(request.user)


class ConfirmCodeRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        request_body=ConfirmCodeRegisterSerializer(),
        operation_description="""
                    `POST` - Подверждение пороля.
                    """
    )
    def post(self, request):
        return confirm_code_register(request)


class ResendConfirmCodeRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
                        `GET` - Отправка снова.
                        """
    )
    def get(self, request):
        return resend_confirm_code_register(request)


class SendResetCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return reset_code(request)


class VerifyResetCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return verify_reset_code(request)


class ResetChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return reset_change_password(request)
#
#
# class NotifyUsersView(APIView):
#     def get(self, request):
#         notify_users_for_subscription.apply_async(countdown=1)  # или определенное время для тестирования
#         return Response("Уведомления запущены")


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
                            `GET` - Получить информацию о подпиське.
                            """
    )
    def get(self, request):
        return subscription_detail(request)

    @swagger_auto_schema(
        responses={200: SubscriptionSerializer()},
        request_body=SubscriptionSerializer(),
        operation_description="""
                `POST` - Подписька.
                нужно отправить конец подпиську
                Например: (2023-12-12)
                """
    )
    def post(self, request):
        return subscription(request)



