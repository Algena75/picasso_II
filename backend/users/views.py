from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (OpenApiExample, extend_schema,
                                   extend_schema_view)
from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import (MeSerializer, SignupSerializer,
                               TokenSerializer, UserSerializer)


@extend_schema(tags=['Пользователи'], summary='Список пользователей')
@extend_schema_view(retrieve=extend_schema(exclude=True))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    @extend_schema(tags=['Пользователи'],
                   summary='Данные пользователя и список его аренд')
    @action(
        detail=False, methods=['get',],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def about_me(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class UserRegView(APIView):
    serializer_class = SignupSerializer

    @extend_schema(
        tags=['Аутентификация'],
        auth=None,
        description='Авторизация',
        examples=[
            OpenApiExample(
                name='Пример пользователя',
                description='Пример для тестирования',
                value={
                    "username": "Vasya",
                    "email": "vasya@mail.ru",
                    "password": "vasya_password"
                }
            )
        ],
        summary='Регистрация нового пользователя'
    )
    def post(self, request):
        data = request.data
        serializer = SignupSerializer(data=data)
        if isinstance(data, QueryDict):
            data = data.dict()
        if User.objects.filter(email=data.get('email')).exists():
            return Response(
                'Учетная запись с таким email уже существует',
                status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            user = User.objects.create(
                **serializer.validated_data
            )
            user.set_password(data.get('password'))
            user.save()
            return Response(
                model_to_dict(user, fields=['username', 'email', 'id']),
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@permission_classes([AllowAny])
class GetTokenView(APIView):
    serializer_class = TokenSerializer

    @extend_schema(
        tags=['Аутентификация'],
        auth=None,
        description='Получение токена.',
        examples=[
            OpenApiExample(
                name='Пример пользователя',
                description='Пример для тестирования',
                value={
                    "email": "vasya@mail.ru",
                    "password": "vasya_password"
                }
            )
        ],
        summary='Получение токена',
        request=TokenSerializer,
    )
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        email = serializer.data['email']
        user = get_object_or_404(User, email=email)
        password = serializer.data['password']
        if not authenticate(username=email, password=password):
            return Response({'Неверные данные'}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)},
                        status=status.HTTP_200_OK)
