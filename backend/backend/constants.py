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
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", 'rent-details')


constants = Constants()
