from __future__ import print_function
from auth import spreadsheet_service
#from auth import drive_service
import random

spreadsheet_id = '1zA-GImkIsmVmwn49PabCoA2dYkCl7S1RfUFDF6Sc_Ec'
last_row = 403 # if new entry is added, 1 added to last_row

# can be used to read one range at a time
def read_range():
    medium = ''
    title = ''
    status = ''
    score = -1
    # add in score function
    # make sure all empty fields contain 'null' on spreadsheet

    #while True:
    rec = random.randint(2, last_row)
    range_name = 'Sheet1!A%d:G%d' % (rec, rec)
    sheetId = '1zA-GImkIsmVmwn49PabCoA2dYkCl7S1RfUFDF6Sc_Ec'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=sheetId, range=range_name).execute()
    rows = result.get('values', [])
    title = rows[0][1]
    medium = rows[0][2]
    status = rows[0][4]
    #if(medium != 'Webtoon' or title == 'null' or status == 'Hiatus'):
    #rec = random.randint(2, last_row)
    #else:
    #break

    creator = rows[0][3]
    genre = rows[0][5]
    score = rows[0][6]

    print('Here is a(n)', medium, 'recommendation for you: ')
    #print('{0} rows retrieved.'.format(len(rows)))
    #print('{0}'.format(rows[0]))
    print('Title:', title)
    if (creator != 'null'):
        print('Creator(s):', creator)
    if (status != 'null'):
        print('Status:', status)
    if (genre != 'null'):
        print('Genre(s):', genre)
    if (int(score) < 0):
        print('This', medium, 'has not yet been scored.')
    else:
        print('Score:', score)

    return rows


read_range()
