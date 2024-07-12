import logging
from datetime import datetime

from google.oauth2.service_account import Credentials
from googleapiclient import discovery

from backend.constants import constants

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

CREDENTIALS = Credentials.from_service_account_info(info=constants.INFO,
                                                    scopes=SCOPES)
SHEETS_SERVICE = discovery.build('sheets', 'v4', credentials=CREDENTIALS)
DRIVE_SERVICE = discovery.build('drive', 'v3', credentials=CREDENTIALS)


def get_list_obj(service=DRIVE_SERVICE):
    response = service.files().list(
        q='mimeType="application/vnd.google-apps.spreadsheet"').execute()
    return response['files']


def set_user_permissions(service, spreadsheetId):
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': constants.EMAIL_USER
    }
    service.permissions().create(
        fileId=spreadsheetId,
        body=permissions_body,
        fields='id'
    ).execute()


def create_spreadsheet(service=SHEETS_SERVICE):
    spreadsheet_body = {
        'properties': {
            'title': 'Rent report',
            'locale': 'ru_RU',
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': f'{datetime.now().year} год',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 8
                }
            }
        }]
    }
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    spreadsheetId = response['spreadsheetId']
    set_user_permissions(DRIVE_SERVICE, spreadsheetId)
    logging.info(f'Создана таблица {spreadsheetId}')
    spreadsheet_update_values(SHEETS_SERVICE,
                              spreadsheetId,
                              constants.TABLE_HEADER_VALUES,
                              default=True)
    return spreadsheetId


def spreadsheet_update_values(service, spreadsheetId, data, default=False):
    if default:
        request = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheetId, body=constants.TABLE_HEADER_SETTINGS
        )
        request.execute()
        table_values = data
    else:
        table_values = read_values(service, spreadsheetId)
        table_values.append(data)

    request_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range="A1:H100",
        valueInputOption="USER_ENTERED",
        body=request_body
    )
    request.execute()
    logging.info(f'Таблица {spreadsheetId} обновлена.')


def read_values(service, spreadsheetId):
    range = "A1:H100"
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range=range,
        valueRenderOption='FORMULA',
    ).execute()
    return response['values']


def clear_disk(service=DRIVE_SERVICE):
    for spreadsheet in get_list_obj(service):
        response = service.files().delete(fileId=spreadsheet['id'])
        response.execute()
    return 'Документы удалены'
