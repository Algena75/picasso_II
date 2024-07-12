import os


class Constants:
    TAX_PER_MINUTE: int = 10

    EMAIL_SUBJECT: str = 'Данные по аренде {id}.'
    EMAIL_TEXT: str = (
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
    ADMIN_EMAIL: str = 'admin@admin.ru'

    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", 'minio:9000')
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ROOT_USER")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_ROOT_PASSWORD")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", 'rent-details')

    EMAIL_USER: str = os.getenv('EMAIL')
    INFO: dict[str, str] = {
        'type': os.getenv('TYPE'),
        'project_id': os.getenv('PROJECT_ID'),
        'private_key_id': os.getenv('PRIVATE_KEY_ID'),
        'private_key': os.getenv('PRIVATE_KEY'),
        'client_email': os.getenv('CLIENT_EMAIL'),
        'client_id': os.getenv('CLIENT_ID'),
        'auth_uri': os.getenv('AUTH_URI'),
        'token_uri': os.getenv('TOKEN_URI'),
        'auth_provider_x509_cert_url': os.getenv(
            'AUTH_PROVIDER_X509_CERT_URL'
        ),
        'client_x509_cert_url': os.getenv('CLIENT_X509_CERT_URL')
    }
    SPREADSHEET_ID: str = os.getenv('SPREADSHEET_ID', None)
    TABLE_HEADER_SETTINGS: dict = {
        'requests': [
            {
                'mergeCells': {
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": 8
                    },
                    "mergeType": "MERGE_ROWS",
                },
            },
            {
                'mergeCells': {
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": 2,
                        "endRowIndex": 3,
                        "startColumnIndex": 0,
                        "endColumnIndex": 8
                    },
                    "mergeType": "MERGE_ALL",
                },
            },
            {
                "repeatCell": {
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": 8
                    },
                    'cell': {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "bold": True
                            }
                        }
                    },
                    'fields': "userEnteredFormat(textFormat,horizontalAlignment)"
                },
            },
            {
                "repeatCell": {
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": 2,
                        "endRowIndex": 3,
                        "startColumnIndex": 0,
                        "endColumnIndex": 8
                    },
                    'cell': {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
                },
            },
            {
                "repeatCell": {
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": 3,
                        "endRowIndex": 4,
                        "startColumnIndex": 0,
                        "endColumnIndex": 8
                    },
                    'cell': {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 50.0,
                                "green": 1.0,
                                "blue": 255.0
                            },
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "foregroundColor": {
                                    "blue": 1.0
                                },
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
                },
            },
            {
                "repeatCell": {
                    'range': {
                        "sheetId": 0,
                        "startRowIndex": 1,
                        "endRowIndex": 2,
                        "startColumnIndex": 1,
                        "endColumnIndex": 2
                    },
                    'cell': {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "foregroundColor": {
                                    "red": 1.0
                                },
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat(textFormat,horizontalAlignment)"
                },
            },
        ],
    }
    TABLE_HEADER_VALUES: list = [
        ['Отчёт по аренде'],
        ['Общая выручка', '=SUM(H5:H100)'],
        ['Список аренд'],
        ['ID', 'User', 'Bicycle', 'Start', 'Finish', 'Duration', 'Price',
         'Value'],
    ]


constants = Constants()
