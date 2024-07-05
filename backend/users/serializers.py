import re

from rest_framework import serializers

from bicycles.serializers import RentSerializer
from users.models import User


class ValidateUserSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        if not re.match(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                f'{value} содержит запрещённые символы.'
            )
        if len(value) > 150:
            raise serializers.ValidationError(
                'Имя пользователя не может быть больше 150 символов.'
            )
        return value


class UserSerializer(ValidateUserSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.CharField(required=True, max_length=254)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'pk'
        )
        ordering = ['-pk']


class SignupSerializer(ValidateUserSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        ordering = ['-pk']


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class MeSerializer(UserSerializer):
    rents = RentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'pk', 'rents'
        )
