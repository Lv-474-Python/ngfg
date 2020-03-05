"""
Google Sheet manager
"""
import os # TODO remove
import httplib2
# import gspread
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# TODO remove
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))
print()


class SheetManager():
    """
    Google sheet manager.
    Can get data from the sheet, append data to the sheet and pretty print data.

    IMPORTANT:
    User must share google sheet with ngfg-account@ngfg-268019.iam.gserviceaccount.com

    """
    # credentials_file = 'app/helper/ngfg-сredentials.json'
    credentials_file = 'ngfg-сredentials.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    SHEETID = '1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM'

    @staticmethod
    def get_data_with_range(spreadsheet_id, from_row, to_row):
        """
        # TODO handle spreadsheet_id error
        Get data from google sheet by sheet id with range

        :param spreadsheet_id: str | google shit id, can be gotten from url
            E.G: https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit#gid=0
                 https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit?usp=sharing
                 https://docs.google.com/spreadsheets/d/1-mUpVrw6TScp5G8HoFJ7JFe9QPpLkUtqWtKIupDtFV4/edit?usp=sharing
            spreadsheet_id = '1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM'
        :param from_row: str | cell to begin with. E.G.: 'a', 'A1', 'b3'
        :param to_row: str | cell where search stop. E.G.: 'c', 'C5', 'c3'
        :return: list of lists or None
        """
        ranges = f'{from_row}:{to_row}'
        values = SheetManager.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=ranges,
            majorDimension='ROWS'
        ).execute()

        data = values.get('values')
        return data

    @staticmethod
    def get_all_data(spreadsheet_id):
        """
        # TODO handle spreadsheet_id error
        Get data from google sheet by sheet id with range

        :param spreadsheet_id: str | google shit id, can be gotten from url
            E.G: https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit#gid=0
            spreadsheet_id = '1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM'
        :return: list of lists or None
        """
        # try:
        values = SheetManager.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A:Z',
            majorDimension='ROWS'
        ).execute()

        data = values.get('values')
        return data
        # except:


    @staticmethod
    def append_data(spreadsheet_id, values):
        """
        # TODO handle spreadsheet_id error

        Append data to google sheet by sheet id

        :param spreadsheet_id: str | google shit id, can be gotten from url
            E.G: https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit#gid=0
            spreadsheet_id = '1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM'
        :param values: iterated data type | data to append
        :return: TODO what to return
        """


        data = [[element] for element in values]

        resource = {
            "majorDimension": "COLUMNS",
            "values": data
        }
        spreadsheetId = spreadsheet_id
        range = "A:A"
        SheetManager.service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId,
            range=range,
            body=resource,
            valueInputOption="USER_ENTERED"
        ).execute()

# Create new spreadsheet
# https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit?usp=sharing

# driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
# shareRes = driveService.permissions().create(
#     fileId = spreadsheet['spreadsheetId'],
#     body = {'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
#     fields = 'id'
# ).execute()

data = SheetManager.get_all_data('1-mUpVrw6TScp5G8HoFJ7JFe9QPpLkUtqWtKIupDtFV4')
pprint(data)
print(type(data))
# data = SheetManager.get_data_with_range('1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM', 'a1', 'f6')

# SheetManager.append_data('1-mUpVrw6TScp5G8HoFJ7JFe9QPpLkUtqWtKIupDtFV4', {"I":1, "Love":2, "You <3":3})
