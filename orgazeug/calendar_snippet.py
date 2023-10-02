import os
import csv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Define the scope and token file
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.json'  # Change this to the path of your token JSON file

# Your CSV file with raw data
CSV_FILE = 'calendar_data.csv'  # Change this to the path of your CSV file

# Function to authenticate and get the Google Calendar service
def authenticate_google_calendar():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

# Function to create calendar events from CSV data
def create_calendar_events(service, csv_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            event = {
                'summary': row['EventTitle'],
                'description': row['EventDescription'],
                'start': {
                    'dateTime': row['EventStart'],
                    'timeZone': 'YourTimeZone',
                },
                'end': {
                    'dateTime': row['EventEnd'],
                    'timeZone': 'YourTimeZone',
                },
            }
            service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event '{event['summary']}' created.")

def main():
    service = authenticate_google_calendar()
    create_calendar_events(service, CSV_FILE)

if __name__ == '__main__':
    main()
