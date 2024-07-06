import pytest


@pytest.fixture
def password():
    return '1234567'


@pytest.fixture
def user(django_user_model, password):
    return django_user_model.objects.create_user(
        username='TestUser',
        email='testuser@email.com',
        password=password
    )


@pytest.fixture
def another_user(django_user_model, password):
    return django_user_model.objects.create_user(
        username='TestUser2',
        email='testuser2@email.com',
        password=password
    )


@pytest.fixture
def token(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    token = RefreshToken.for_user(user)
    return token.access_token


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client
