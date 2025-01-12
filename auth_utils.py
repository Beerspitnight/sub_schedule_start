# auth_utils.py

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import gspread

def authenticate_google_apis():
    """
    Authenticates with Google using a service account JSON file.
    Expects the environment variable GOOGLE_APPLICATION_CREDENTIALS to be set.
    Returns:
        drive_service (Resource): Google Drive API resource
        docs_service (Resource): Google Docs API resource
        sheets_client (gspread.Client): GSpread client for Sheets
    """
    credentials = Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/documents.readonly"
        ]
    )

    drive_service = build("drive", "v3", credentials=credentials)
    docs_service = build("docs", "v1", credentials=credentials)
    sheets_client = gspread.authorize(credentials)

    return drive_service, docs_service, sheets_client
