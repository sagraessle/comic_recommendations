from __future__ import print_function
from auth import spreadsheet_service
#from auth import drive_service
import hashlib
import os
import random
import sys
import linecache
import ast

spreadsheet_id = '1zA-GImkIsmVmwn49PabCoA2dYkCl7S1RfUFDF6Sc_Ec'


def recommend(genre):
    last_row = 403
    medium = ''
    title = ''
    status = ''
    score = -1
    # add in score function
    # make sure all empty fields contain 'null' on spreadsheet

    range_name = 'Sheet1!A%d:H%d' % (1, last_row)
    sheetId = '1zA-GImkIsmVmwn49PabCoA2dYkCl7S1RfUFDF6Sc_Ec'
    result = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=sheetId, range=range_name).execute()
    rows = result.get('values', [])

    #print entire sheet to file 'local.txt'
    original_stdout = sys.stdout
    with open('node_modules/.local.txt', 'w') as f:
        sys.stdout = f
        for r in rows:
            print(str(r))
        sys.stdout = original_stdout
    f.close()

    # Will cycle through for a webtoon/manga with score >= 6, has a title, and not on hiatus
    while (int(score) <= 6 or (medium != 'webtoon' and medium != 'manga')
           or title == 'null' or status == 'hiatus'):
        # random number from the range of line numbers in 'local.txt'
        rand = random.randint(2, last_row)

        # fetch the random line from 'local.txt'
        line = linecache.getline(r"node_modules/.local.txt", rand)

        # the line string will be put into rec as a list
        rec = ast.literal_eval(line)

        title = rec[1]
        medium = rec[2]
        status = rec[4]
        score = rec[6]

    creator = rec[3]
    genre = rec[5]
    note = rec[7]

    print('Here is a', medium, 'recommendation for you: ')
    print('Title:', title)
    if (creator != 'null'):
        print('Creator(s):', creator)
    if (status != 'null'):
        print('Status:', status)
    if (genre != 'null'):
        print('Genre(s):', genre)
    #print('Score:', score)
    if (note != 'null'):
        print('\n', note)

    return rows


def addEntry():
    auth()
    print('This option has not yet been implemented.')


def editEntry():
    auth()
    print('This option has not yet been implemented.')


def auth():
    user = input('Enter admin username: ')
    attempt = input('Enter admin password: ')

    # search through for username in node_modules/passwd file
    # if username is not found, or username found but wrong password,
    # print that username or password is wrong
    # if user makes three wrong attempts, cancel operation
    # if password hash of 'attempt' matches that of the user pass in file, authenticate

    # https://nitratine.net/blog/post/how-to-hash-passwords-in-python/


def addUser():
    # add a new user and password hash to password file
    salt = os.urandom(32)

    # need to go through and check whether username is already taken
    user = input('Create a username: ')
    password = input('Enter a password: ')

    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    original_stdout = sys.stdout
    with open('.passwd', 'w') as f:
        sys.stdout = f
        print('[', user, ',', key, ']')
        sys.stdout = original_stdout
    f.close()

    # when new user is successfully added, print the following
    print('New user successfully added!\n')


def main():
    print('\t\t\t*************')
    print('\t\t\tStory Manager')
    print('\t\t\t*************\n')

    print('Make a selection:')
    # option to get a recomendation based on genre
    # option to add a new entry, must insert to sheet in alphabetical order or reorder sheet to order after adding
    # option to modify a current entry (list all webtoon/manga names to choose from)
    print('a: Random webtoon or manga recommendation.')
    print('b: Recommend webtoon or manga by genre.')
    print('c: Add a new entry.')  # password required
    print('d: Edit existing entry.')  # password required
    choice = input('')
    print('')

    if (choice == 'a'):
        recommend('null')
    elif (choice == 'b'):
        genre_selection = [
            'action', 'comedy', 'drama', 'fantasy', 'heartwarming',
            'historical', 'horror', 'isekai', 'romance', 'sci-fi',
            'slice of life', 'supernatural', 'thriller'
        ]
        for g in genre_selection:
            print(g)
        genre = input(
            '\nSelect a genre from the list above: '
        )  # only accept valid genres from genre_selection list as input
        print('')
        recommend(genre)
    elif (choice == 'c'):
        addEntry()
    elif (choice == 'd'):
        editEntry()
    elif (choice == 'add new user'):  # comment this out when not needed
        addUser()
    else:
        print('Error: Invalid selection!')

    # make a system where higher chance to recommend with higher scoring


main()
