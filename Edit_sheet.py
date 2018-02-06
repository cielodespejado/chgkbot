import httplib2
import argparse
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import time
from collections import namedtuple

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
def get_credentials():
    store = Storage('googleapi.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
    return credentials

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
service = discovery.build('sheets', 'v4', http = http, discoveryServiceUrl = discoveryUrl)
spreadsheetId = '1zdjZ5UCNZSVlp_R_4DxOm4JFGxsguiSyaIaOON5hB0o'

DB = {}
db = namedtuple('db', 'year1 year2 author')

def edit_sheet(cid, DB):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='A2:A', majorDimension='ROWS').execute()
    values = result.get('values')
    for i,k in enumerate(values,2):
        if int(*k) == cid:
            rang = 'A'+str(i)+':D'+str(i)
    body = {'data':[{'range':rang,'values':[[cid] + list(tuple(DB[cid]))],'majorDimension':'ROWS'}], 'valueInputOption':'RAW'}     
    edit = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='A2:D', majorDimension='ROWS').execute()
    values = result.get('values')
    for i in values:
        DB[int(i[0])] = db(i[1],i[2],i[3])
    return DB    

def add_to_sheet(cid):
    body = {'range':'A2:D','majorDimension':'ROWS','values':[[cid, '2007', str(time.gmtime().tm_year),'None']]}
    app = service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range='A2:D', valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body).execute()
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='A2:D', majorDimension='ROWS').execute()
    values = result.get('values')
    for i in values:
        DB[int(i[0])] = db(i[1],i[2],i[3])
    return DB       
