from backend.constants import constants
from bicycles.google_services import SHEETS_SERVICE


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


def spreadsheet_update_values(service, spreadsheetId, data):
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


def read_values(service, spreadsheetId):
    range = "A1:H100"
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range=range,
        valueRenderOption='FORMULA',
    ).execute()
    return response['values']


def make_record(data: list):
    return spreadsheet_update_values(SHEETS_SERVICE, constants.SPREADSHEET_ID,
                                     data)
