from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import smtplib
import configparser


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_file = os.path.join(os.path.dirname(__file__), 'token.json')
    creds_file = os.path.join(os.path.dirname(__file__), 'credentials.json')
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    page_token = None
    results = service.files().list(q="fullText contains 'followup:actionitems' and trashed = false",
                                   pageSize=50,
                                   pageToken=page_token,
                                   fields="nextPageToken, files(name, webViewLink)").execute()
    items = results.get('files', [])

    items_list = []
    if not items:
        print('No files found.')
    else:
        print('Files where you are assigned an action item:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['webViewLink']))
            items_list.append(u'{0} ({1})'.format(item['name'], item['webViewLink']))
        
        send_email(items_list)


def send_email(message):
    port = config.getint('default', 'mail_server_port')
    smtp_server = config.get('default', 'mail_server')
    sender_email = config.get('default', 'mail_from')
    receiver_email = config.get('default', 'mail_to')
    subject = config.get('default', 'mail_subject')

    msg = f"From: {sender_email}\nTo: {receiver_email}\n"
    msg += f"Subject: {subject}\n"
    for line in message:
        msg += f"* {line}\n\n"

    server = smtplib.SMTP(smtp_server, port)
    # server.set_debuglevel(1)
    server.sendmail(sender_email, [receiver_email], msg)
    server.quit()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'reminder.conf'))
    main()
