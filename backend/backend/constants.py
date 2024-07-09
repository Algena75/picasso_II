import os


class Constants:
    TAX_PER_MINUTE = 10

    EMAIL_SUBJECT = 'Данные по аренде {id}.'
    EMAIL_TEXT = (
        'Уважаемый {name}!'
        'Данные по аренде {id}:\n\n'
        '1. Арендован велоспед {bike}.\n'
        '2. Начало аренды: {start}\n'
        '3. Окончание аренды: {finish}\n'
        '4. Длительность аренды составила {rent_duration} мин.\n'
        '5. Стоимость аренды составила {value} руб.\n\n'
        'Благодарим Вас за то, что воспользовались нашим сервисом и будем рады '
        'видеть Вас снова!'
    )
    ADMIN_EMAIL = 'admin@admin.ru'

    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", 'minio:9000')
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ROOT_USER")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_ROOT_PASSWORD")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", 'rent-details')

    EMAIL_USER = os.getenv('EMAIL')
    INFO = {
        'type':  os.getenv('TYPE'),
        'project_id':  os.getenv('PROJECT_ID'),
        'private_key_id':  os.getenv('PRIVATE_KEY_ID'),
        'private_key':  os.getenv('PRIVATE_KEY'),
        'client_email':  os.getenv('CLIENT_EMAIL'),
        'client_id':  os.getenv('CLIENT_ID'),
        'auth_uri':  os.getenv('AUTH_URI'),
        'token_uri':  os.getenv('TOKEN_URI'),
        'auth_provider_x509_cert_url':  os.getenv(
            'AUTH_PROVIDER_X509_CERT_URL'
        ),
        'client_x509_cert_url':  os.getenv('CLIENT_X509_CERT_URL')
    }
    SPREADSHEET_ID: str = os.getenv('SPREADSHEET_ID')


constants = Constants()
