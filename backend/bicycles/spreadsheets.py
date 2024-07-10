import logging

from backend.constants import constants
from bicycles.google_services import (SHEETS_SERVICE, clear_disk,
                                      create_spreadsheet, get_list_obj,
                                      spreadsheet_update_values)


def make_record(data: list, clear: bool = False):
    try:
        if clear:
            clear_disk()
        if constants.SPREADSHEET_ID is None:
            spreadsheet_ids = get_list_obj()
            if spreadsheet_ids:
                spreadsheet_id = spreadsheet_ids[0].get('id')
            else:
                spreadsheet_id = create_spreadsheet()
            constants.SPREADSHEET_ID = spreadsheet_id
        return spreadsheet_update_values(SHEETS_SERVICE, constants.SPREADSHEET_ID,
                                         data)
    except Exception as error:
        return logging.error(f'Google Sheets are unavailable\n{error}')
