from __future__ import print_function
from auth import spreadsheet_service
from auth import drive_service

spreadsheet_id = ''
def create():
    spreadsheet_details = {
    'properties': {
        'title': 'Python-google-sheets-demo'
        }
    }
    sheet = spreadsheet_service.spreadsheets().create(body=spreadsheet_details,
                                    fields='spreadsheetId').execute()
    global spreadsheet_id
    spreadsheet_id = sheet.get('spreadsheetId')
    print('Spreadsheet ID: {0}'.format(spreadsheet_id))
    permission1 = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': 'EMAIL'
    }
    drive_service.permissions().create(fileId=spreadsheet_id, body=permission1).execute()
    return spreadsheet_id
def read_range():
    range_name = 'Sheet1!A1:H1'
    sheetId = '1JCEHwIa4ZzwAiKGmAnWGfbjeVCH_tWZF6MkIU0zICwM'
    result = spreadsheet_service.spreadsheets().values().get(
    spreadsheetId=sheetId, range=range_name).execute()
    rows = result.get('values', [])
    print('{0} rows retrieved.'.format(len(rows)))
    print('{0} rows retrieved.'.format(rows))
    return rows
def write_range():
    create()
    range_name = 'Sheet1!A1:H1'
    values = read_range()
    value_input_option = 'USER_ENTERED'
    body = {
        'values': values
    }
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))
def read_ranges():
    write_range()
    sheetId = '1JCEHwIa4ZzwAiKGmAnWGfbjeVCH_tWZF6MkIU0zICwM'
    range_names = ['Sheet1!A2:H21', 'Sheet1!A42:H62']
    result = spreadsheet_service.spreadsheets().values().batchGet(
     spreadsheetId=sheetId, ranges=range_names).execute()
    ranges = result.get('valueRanges', [])
    print('{0} ranges retrieved.'.format(len(ranges)))
    return ranges

def write_ranges():
    values = read_ranges()
    data = [
        {
            'range': 'Sheet1!A2:H21',
            'values': values[0]['values']
        },
       {
            'range': 'Sheet1!A22:H42',
            'values': values[1]['values']
        }
    ]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    result = spreadsheet_service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
write_ranges()