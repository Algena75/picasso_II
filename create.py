from google.oauth2.service_account import Credentials
from googleapiclient import discovery 

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

CREDENTIALS_FILE = 'rent-a-bicycle-service-ff9d405770ba.json'

def auth():
    # Создаём экземпляр класса Credentials.
    credentials = Credentials.from_service_account_file(
                  filename=CREDENTIALS_FILE, scopes=SCOPES)
    # Создаём экземпляр класса Resource.
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service, credentials


def create_spreadsheet(service):
    spreadsheet_body = {
        'properties': {
            'title': 'Rent report',
            'locale': 'ru_RU',
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': '2024 год',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 10
                }
            }
        }]
    }
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    spreadsheet_id = response['spreadsheetId']
    print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
    return spreadsheet_id


def set_user_permissions(spreadsheet_id, credentials):
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': 'alex.naumov812@gmail.com'
    }
    drive_service = discovery.build('drive', 'v3', credentials=credentials)
    
    drive_service.permissions().create(
        fileId=spreadsheet_id,
        body=permissions_body,
        fields='id'
    ).execute()


def spreadsheet_update_values(service, spreadsheetId):
    table_values = [
        ['Отчёт по аренде'],
        ['Общая выручка', '=SUM(H5:H100)'],
        ['Список аренд'],
        ['ID', 'User', 'Bicycle', 'Start', 'Finish', 'Duration', 'Price',
         'Value'],
    ]
    request_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range="A1:H30",
        valueInputOption="USER_ENTERED",
        body=request_body
    )
    request.execute()


service, credentials = auth()
spreadsheetId = '1dMBD6HgbQ7rdhLb9DAylTVvEZGMu8yxXT5ZO7CQBxp8'  # create_spreadsheet(service)
# set_user_permissions(spreadsheetId, credentials)
spreadsheet_update_values(service, spreadsheetId)
