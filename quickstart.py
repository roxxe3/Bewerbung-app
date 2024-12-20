import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

today = datetime.date.today().strftime('%Y-%m-%d')

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "16akauCRJY2YR474psu-1Wxfb4Aoz2xUTv6rs2ewqaYU"
SAMPLE_RANGE_NAME = "Class Data!A2:E"

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def parse_email(email):
    name = ""
    for i in range(len(email)):
        if email[i] == "@":
            name = email[i + 1: len(email)]
            return name




def append_data(ausbildung, email):
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        name = parse_email(email)
        
        body = {
            'values': [
                [ausbildung ,email, f'=TODAY()', name]
            ]
        }
        
        result = service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="Job Tracker Spreadsheet!E:E",
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        # Print entire result for debugging
        print("Response:", result)
        
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
        
    except HttpError as err:
        print(f"An error occurred: {err}")
        print(f"Error details: {err.error_details}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




def clear_excess_data():
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        
        # Clear from row 16 onward to reset any residual data
        clear_range = "Job Tracker Spreadsheet!A16:Z"
        
        service.spreadsheets().values().clear(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=clear_range
        ).execute()
        
        print("Cleared excess data beyond row 16.")
    except HttpError as err:
        print(f"An error occurred: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print(parse_email("bewerbungen@destatis.de"))