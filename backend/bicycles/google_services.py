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
