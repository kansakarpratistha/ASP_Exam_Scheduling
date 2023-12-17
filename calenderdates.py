from __future__ import print_function
import datetime
import os.path

from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class EventsExtract():
    def main(self):
        creds = None
        event_times = []
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    
        try:
            service = build('calendar', 'v3', credentials=creds)

            now = datetime.datetime.utcnow().isoformat()+ 'Z'
            events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return []

            for event in events:
                event_time = event['start'].get('dateTime', event['start'].get('date'))
                event_times.append(datetime.datetime.fromisoformat(event_time).date())
        
            
            return event_times

        except HttpError as error:
            print('Error has occurred: %s' % error)


