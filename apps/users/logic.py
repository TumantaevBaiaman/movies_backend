import secrets
import smtplib
import string
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.favorites.models import Favorite
from apps.users.models import User, Subscription, Notification
from apps.users.serializers import UserRegisterSerializer, UserSerializer, ResetChangePasswordSerializer, \
    LoginUserSerializer, SubscriptionCreateSerializer, SubscriptionSerializer, NotificationSerializer


def send_confirmation_code_email(user_email, confirmation_code):

    try:
        subject = "КОД ПОДВЕРЖДЕНИЕ"
        message = f"{confirmation_code}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)
        return True

    except Exception as e:
        print(f'Ошибка отправки электронной почты: {e}')
        return False


def generate_confirmation_code(length=4):
    characters = string.digits
    temporary_password = ''.join(secrets.choice(characters) for _ in range(length))
    return temporary_password


def create_user(data):
    serializer = UserRegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.confirmation_code_created_at = timezone.now()
        Favorite.objects.create(user=user).save()
        user.save()
        send = send_confirmation_code_email(user_email=serializer.validated_data.get("email"), confirmation_code=confirmation_code)
        if send:
            return None, user
        else:
            return Response({'error': "Возникли ошибки при отправке на почту"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return serializer.errors, None


def create_tokens(user):
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)
    access_token_expiration = (datetime.utcnow() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
    refresh_token_expiration = (datetime.utcnow() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

    return {
        'access': str(access_token),
        'refresh': str(refresh_token),
        'access_token_expiration': access_token_expiration,
        'refresh_token_expiration': refresh_token_expiration,
    }


def create_user_with_tokens(request):
    err, user = create_user(request.data)
    if user:
        tokens = create_tokens(user)
        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin,
        }
        response_data = {
            'detail': 'Вас было отправлено код подверждение!',
            **tokens,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(err, status=status.HTTP_400_BAD_REQUEST)


def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user is not None:
        user_serializer = UserSerializer(instance=user)
        tokens = create_tokens(user)
        if user.email_verify:
            response_data = {
                'success': 'Успешно!',
                'verify': True,
                'user': user_serializer.data,
                **tokens,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            confirmation_code = generate_confirmation_code()
            user.confirmation_code = confirmation_code
            user.confirmation_code_created_at = timezone.now()
            user.save()
            send = send_confirmation_code_email(user_email=email,
                                                confirmation_code=confirmation_code)
            response_data = {
                'success': 'Вы ещё не подвердили код водверждение, вам было отправлено код подверждение!',
                'verify': False,
                'user': user_serializer.data,
                **tokens,
            }
            if send:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': "Возникли ошибки при отправке на почту"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


def confirm_code_register(request):
    confirmation_code = request.data.get('confirmation_code')
    user = request.user

    if user.confirmation_code == confirmation_code:
        if (timezone.now() - user.confirmation_code_created_at) < timedelta(minutes=2):
            user.email_verify = True
            user.confirmation_code = None
            user.confirmation_code_created_at = None
            user.save()
            user_serializer = UserSerializer(instance=user)
            return Response({'message': 'Адрес электронной почты подтвержден', 'user': user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Срок действия кода подтверждения истек'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Неправильный код подтверждения'}, status=status.HTTP_400_BAD_REQUEST)


def resend_confirm_code_register(request):
    user = request.user
    confirmation_code = generate_confirmation_code()
    user.confirmation_code = confirmation_code
    user.confirmation_code_created_at = timezone.now()
    user.save()
    send = send_confirmation_code_email(user_email=user.email, confirmation_code=confirmation_code)
    if send:
        return Response({"message": "Вам было отправлено повторный код"}, status=status.HTTP_200_OK)
    else:
        return Response({'error': "Возникли ошибки при отправке на почту"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def reset_code(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        moments_time = timezone.now()
        code = generate_confirmation_code()
        user.confirmation_code = code
        user.confirmation_code_created_at = moments_time
        user.save()
        send = send_confirmation_code_email(user_email=user.email, confirmation_code=code)
        if send:
            return Response(
                {
                    "message": "Код отправлен на вашу почту",
                }, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Возникли ошибки при отправке на почту"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Пользователь с таким email не найден'}, status=status.HTTP_404_NOT_FOUND)


def verify_reset_code(request):
    email = request.data["email"]
    verify_code = request.data.get("verify_code")
    user = User.objects.filter(email=email).first()
    if user:
        user_confirm = User.objects.get(email=email)
        code = user_confirm.confirmation_code
        user_token = create_tokens(user_confirm)
        if (timezone.now() - user.confirmation_code_created_at) < timedelta(minutes=2):
            if code == verify_code:
                return Response(
                    {
                        "message": "Код подвержден теперь измените ваш пароль",
                        **user_token
                    }, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Срок действия кода подтверждения истек'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Пользователь с таким email не найден'}, status=status.HTTP_404_NOT_FOUND)


def reset_change_password(request):
    serializer = ResetChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'success': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def profile_user(user):
    serializer_user = UserSerializer(instance=user)
    return Response(serializer_user.data, status=status.HTTP_200_OK)


def subscription(request):
    user = request.user
    data = request.data

    try:
        subscription = Subscription.objects.get(user=user)
    except Subscription.DoesNotExist:
        subscription = Subscription.objects.create(user=user)

    subscription.ended_at = data["ended_at"]
    subscription.is_activ = True
    subscription.save()

    serializer = SubscriptionSerializer(instance=subscription)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


def subscription_detail(request):
    user = request.user

    try:
        subscription = Subscription.objects.get(user=user)
    except Subscription.DoesNotExist:
        subscription = Subscription.objects.create(user=user)

    serializer = SubscriptionSerializer(instance=subscription)

    return Response(serializer.data, status=status.HTTP_200_OK)


def notification_list(request):
    user = request.user
    notifications = Notification.objects.filter(users=user)
    serializer = NotificationSerializer(instance=notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def notification_detail(request, id):
    user = request.user
    notifications = get_object_or_404(Notification, id=id)
    notifications.read_notification(user)
    serializer = NotificationSerializer(instance=notifications)
    return Response(serializer.data, status=status.HTTP_200_OK)







