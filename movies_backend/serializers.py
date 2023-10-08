from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):   # noqa
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        user = self.user
        data['user_id'] = user.id
        data['username'] = user.username

        return data
