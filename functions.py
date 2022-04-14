import math
import os
import datetime
from random import random
# Google Sheets API Setup
import gspread
import bcrypt
from oauth2client.service_account import ServiceAccountCredentials

credential = ServiceAccountCredentials.from_json_keyfile_name(
    "qr-attendence.json", [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets"
    ])
client = gspread.authorize(credential)
spreadhseetId = '1Vyxb199JJZGeFIN2H0EE_r4V2SV2lhmSL_WipnA2ay0'
spreadsheet = client.open_by_key(spreadhseetId)

# for sheet in spreadsheet.worksheets():
#     print('sheetName: {}, sheetId(GID): {}'.format(sheet.title, sheet.id))


def get_sheet(sheet_name):
    return spreadsheet.worksheet(sheet_name)


def create_atten_sheet():
    sheet_name = datetime.datetime.now().strftime("%m-%Y")
    if sheet_name in [sheet.title for sheet in spreadsheet.worksheets()]:
        print(
            "Sheet {sheet_name} already exists".format(sheet_name=sheet_name))
        return get_sheet(sheet_name)
    headerValues = [
        "userId", "name", "batch", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
        "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"
    ]
    new_sheet = spreadsheet.add_worksheet(sheet_name, 300, len(headerValues))
    new_sheet.append_row(headerValues)
    master_sheet = get_sheet('master')
    # for each row in master sheet
    for row in master_sheet.get_all_records():
        new_row = []
        new_row.append(row['userId'])
        new_row.append(row['name'])
        new_row.append(row['batch'])
        new_sheet.append_row(new_row)

    return new_sheet


def mark_atten(userId, day, status):
    sheet = create_atten_sheet()
    syncMastersheet(sheet)
    row = sheet.find(userId)
    if row is None:
        return False
    col = day + 3
    sheet.update_cell(row.row, col, status)
    return True


def get_users():
    master_sheet = get_sheet('master')
    users = {}
    for row in master_sheet.get_all_records():
        users.update({
            row['userId']:
            bcrypt.hashpw(
                str(row['password']).encode("utf-8"), bcrypt.gensalt())
        })
    return users

def syncMastersheet(sheet):
    master_sheet = get_sheet('master')
    master_records = master_sheet.get_all_records()
    sheet_records = sheet.get_all_records()
    if len(master_records) != len(sheet_records):
    # sheet = create_atten_sheet()
        i=2
        for row in master_records:
            #sheet.append_row(new_row,table_range='A'+str(i)+':C'+str(i))
            sheet.update('A'+str(i),row['userId'])
            sheet.update('B'+str(i),row['name'])
            sheet.update('C'+str(i),row['batch'])
            i+=1
        print("Master Sheet Synced With "+sheet.title) 
    else:     
        print("Master Sheet Not Synced, Sheet Size Matches with Master Sheet")

