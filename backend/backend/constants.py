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


constants = Constants()
