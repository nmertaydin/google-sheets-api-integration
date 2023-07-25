import os
import random
import uuid

from apiclient import discovery
from google.oauth2 import service_account
from faker import Faker

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials_file = os.path.join(os.getcwd(), 'credentials.json')

spreadsheet_id = 'spreadsheet_id'
range_region = 'Sheet1!A2:F100'

credentials = service_account.Credentials.from_service_account_file(filename=credentials_file, scopes=scopes)
service = discovery.build('sheets', 'v4', credentials=credentials)

# Clear sheet contents
rangeAll = 'Sheet1!A2:Z'
body = {}
resultClear = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=rangeAll, body=body).execute()

# Generate mock data
fake = Faker()
values = []

for i in range(99):
    name = fake.first_name()
    surname = fake.last_name()
    email = '{}.{}@{}'.format(name, surname, fake.domain_name())
    spoken_language = random.choice(['Turkish', 'English', 'German', 'Spanish'])
    is_active = random.choice([True, False])
    id = str(uuid.uuid1())
    values.append([name, surname, email, spoken_language, is_active, id])

body = {
        'values' : values 
    }

service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=body, range=range_region, valueInputOption='USER_ENTERED').execute()

# Get and print sheet contents
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, 
    range=range_region, 
    majorDimension='COLUMNS').execute()

print(result)
