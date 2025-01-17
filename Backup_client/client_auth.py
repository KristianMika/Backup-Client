from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import util

SCOPES = ['https://www.googleapis.com/auth/drive']


def authenticate(cred_dir):
    """ Authenticates against Google Drive API """

    pickle_path = os.path.join(cred_dir, 'token.pickle')
    creds = None

    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        cred_path = os.path.join(cred_dir, 'credentials.json')

        if not os.path.exists(cred_path):
            util.ColorPrinter.print_fail("Couldn't locate \"credentials.json\".\nTerminating...")
            exit(1)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(pickle_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)
