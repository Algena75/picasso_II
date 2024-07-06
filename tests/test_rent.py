from http import HTTPStatus

import pytest

from bicycles.models import Bicycle, Rent


@pytest.mark.django_db(transaction=True)
class TestRentAPI:
    VALID_DATA = {'text': 'Поменяли текст статьи'}

    def test_bicycle_not_found(self, client, bicycle):
        response = client.get('/api/bicycles/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Страница `/api/bicycles/` не найдена, проверьте этот адрес в '
            '*urls.py*.'
        )

    def test_bicycle_not_auth(self, client, bicycle):
        response = client.get('/api/bicycles/')

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что при GET-запросе неавторизованного пользователя к '
            '`/api/bicycles/` возвращается ответ со статусом 401.'
        )

    def test_bicycles_auth_get(self, user_client, bicycle, bicycle_2):
        response = user_client.get('/api/bicycles/')
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что для авторизованного пользователя GET-запрос к '
            '`/api/bicycles/` возвращает статус 200.'
        )

        test_data = response.json()
        assert isinstance(test_data, list), (
            'Проверьте, что для авторизованного пользователя GET-запрос к '
            '`/api/bicycles/` возвращает список.'
        )
        print(len(test_data), test_data)
        assert len(test_data) == Bicycle.objects.filter(is_rented=False).count(), (
            'Проверьте, что для авторизованного пользователя GET-запрос к '
            '`/api/bicycles/` возвращает список всех свободных велосипедов.'
        )

    def test_auth_client_can_rent_bicycle(self, user_client, bicycle):
        bicycles_count = Bicycle.objects.filter(is_rented=False).count()
        response = user_client.get(f'/api/rent/{bicycle.number}/')
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что для авторизованного пользователя get-запрос с '
            'к `/api/rent/{bicycle.number}/` возвращает ответ со '
            'статусом 201.'
        )
        assert bicycles_count > Bicycle.objects.filter(is_rented=False).count(), (
            'Проверьте, что get-запрос к `/api/rent/{bicycle.number}/` уменьшает '
            'количество свободных велосипедов.'
        )

    def test_auth_client_cant_rent_2nd_bicycle(self, user_client, bicycle, bicycle_2):
        user_client.get(f'/api/rent/{bicycle.number}/')
        response = user_client.get(f'/api/rent/{bicycle_2.number}/')
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что авторизованный пользователь не может арендовать '
            'более одного велосипеда.'
        )

    def test_auth_client_can_finish_rent(self, user_client, bicycle):
        user_client.get(f'/api/rent/{bicycle.number}/')
        bicycles_count = Bicycle.objects.filter(is_rented=False).count()
        response = user_client.get(f'/api/finish/{bicycle.number}/')
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что для авторизованного пользователя get-запрос с '
            'к `/api/finish/{bicycle.number}/` возвращает ответ со '
            'статусом 200.'
        )
        assert bicycles_count < Bicycle.objects.filter(is_rented=False).count(), (
            'Проверьте, что get-запрос к `/api/finish/{bicycle.number}/` увеличивает '
            'количество свободных велосипедов.'
        )

    def test_auth_client_cant_finish_rent_2nd_bike(self, user_client, bicycle, bicycle_2):
        user_client.get(f'/api/rent/{bicycle.number}/')
        response = user_client.get(f'/api/finish/{bicycle_2.number}/')
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что авторизованный пользователь не может завершить'
            'аренду другого велосипеда.'
        )
