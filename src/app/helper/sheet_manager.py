"""
Google Sheet manager
"""
import googleapiclient
import httplib2
import apiclient.discovery  # pylint: disable=import-error
from oauth2client.service_account import ServiceAccountCredentials
from app import SHEET_LOGGER


class SheetManager():
    """
    Google sheet manager.
    Can get data from the sheet, append data to the sheet and pretty print data.

    IMPORTANT:
    User must share google sheet with ngfg-account@ngfg-268019.iam.gserviceaccount.com
    Or give editing access url

    """
    credentials_file = 'app/ngfg-сredentials.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    @staticmethod
    def get_data_with_range(spreadsheet_id, from_row, to_row):
        """
        Get data from google sheet by sheet id with range

        :param spreadsheet_id: str | google shit id, can be gotten from url
            E.G: https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUE/edit#gid=0
            spreadsheet_id = '1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUE'
        :param from_row: str | cell to begin with. E.G.: 'a', 'A1', 'b3'
        :param to_row: str | cell where search stop. E.G.: 'c', 'C5', 'c3'
        :return: list of lists or None
        """
        try:
            ranges = f'{from_row}:{to_row}'
            values = SheetManager.service.spreadsheets().values().get(  # pylint: disable=no-member
                spreadsheetId=spreadsheet_id,
                range=ranges,
                majorDimension='ROWS'
            ).execute()

            data = values.get('values')
            return data

        except googleapiclient.errors.HttpError as error:
            SHEET_LOGGER.warning('Error, message: %s', error)
            return None

    @staticmethod
    def get_all_data(spreadsheet_id):
        """
        Get all data from google sheet by sheet id

        :param spreadsheet_id: str | google shit id, can be gotten from url
            E.G: https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUE/edit#gid=0
            spreadsheet_id = '1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUE
        :return: list of lists or None
        """
        try:
            values = SheetManager.service.spreadsheets().values().get(  # pylint: disable=no-member
                spreadsheetId=spreadsheet_id,
                range='A:Z',
                majorDimension='ROWS'
            ).execute()

            data = values.get('values')
            return data
        except googleapiclient.errors.HttpError as error:
            SHEET_LOGGER.warning('Error, message: %s', error)
            return None

    @staticmethod
    def append_data(spreadsheet_id, values: list):
        """
        Append data to google sheet by sheet id

        :param spreadsheet_id: str | google shit id, can be gotten from url
            E.G: https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUE/edit#gid=0
            spreadsheet_id = '1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUE
        :param values: List | data to append
        :return: True or None
        """
        try:
            if not isinstance(values, list):
                SHEET_LOGGER.warning('Someone tried to transfer values not in list')
                return None

            data = [[element] for element in values]
            resource = {
                "majorDimension": "COLUMNS",
                "values": data
            }
            SheetManager.service.spreadsheets().values().append(  # pylint: disable=no-member
                spreadsheetId=spreadsheet_id,
                range='A:A',
                body=resource,
                valueInputOption="USER_ENTERED"
            ).execute()

            return True

        except googleapiclient.errors.HttpError as error:
            SHEET_LOGGER.warning('Error, message: %s', error)
            return None
