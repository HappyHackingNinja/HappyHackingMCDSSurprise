import httplib2
import os
import base64

from apiclient import discovery, errors
import oauth2client
from oauth2client import client
from oauth2client import tools

import sys

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
SAVED_CREDENTIALS = 'saved_credentials.json'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = os.path.join(SAVED_CREDENTIALS)
    print(credential_path)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def active_then_delete():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    list_results = service.users().messages().list(userId='me', q='from:no-reply@mcdonaldssurprise.com').execute()
    messages = list_results.get('messages', [])

    http = httplib2.Http()
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            get_results = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = get_results.get('payload', [])
            email = 'me'
            for header in payload['headers']:
                if header['name'] == 'Delivered-To':
                    email = header['value']
                    continue
            body_data = base64.b64decode(payload['body']['data'].replace('-', '+').replace('_', '/')).decode("utf-8")
            if "https://iw2.mcdonaldssurprise.com/account/activate?token=" in body_data:
                url_activate = body_data[body_data.find('"') + 1: body_data.find('"', body_data.find('https'))]
                resp, content = http.request(url_activate)
                # print(message['id'], email, resp, content)
                try:
                    service.users().messages().delete(userId='me', id=message['id']).execute()
                    sys.stdout.write("帳號: {} 已繳活且刪除其郵件\n\n".format(email))
                except errors.HttpError as error:
                    print('An error occurred: {}'.format(error))

if __name__ == '__main__':
    active_then_delete()