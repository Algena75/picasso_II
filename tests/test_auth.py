from http import HTTPStatus


class TestAuthAPI:

    def test_auth(self, client, user, password):
        response = client.post(
            '/api/token/',
            data={'email': user.email, 'password': password}
        )
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Страница `/api/token/` не найдена, проверьте этот '
            'адрес в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что POST-запрос к `/api/token/` '
            'возвращает ответ с кодом 200.'
        )

        auth_data = response.json()
        assert 'token' in auth_data, (
            'Проверьте, что ответ на POST-запрос с валидными данными к '
            '`/api/token/` содержит токен.'
        )

    def test_auth_with_invalid_data(self, client, user):
        response = client.post('/api/token/', data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что POST-запрос к `/api/token/` '
            'с некорректными данными возвращает ответ со статусовм 400.'
        )
