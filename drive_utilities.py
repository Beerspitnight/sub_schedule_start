# drive_utils.py

import os
from googleapiclient.http import MediaIoBaseDownload
from io import FileIO

def get_latest_docx_in_folder(folder_id, drive_service, filename_contains="Aesop.docx"):
    """
    Searches a Google Drive folder for files containing 'Aesop.docx' in the name,
    and returns the file ID of the most recently modified file that matches.

    Args:
        folder_id (str): The ID of the Drive folder to search in.
        drive_service (Resource): Authenticated Drive API service.
        filename_contains (str): Partial name to filter by (default 'Aesop.docx').

    Returns:
        str: The file ID of the latest matching file, or None if none found.
    """
    query = f"'{folder_id}' in parents and name contains '{filename_contains}' and trashed=false"
    response = drive_service.files().list(
        q=query,
        orderBy="modifiedTime desc",
        fields="files(id, name, modifiedTime)",
        pageSize=1
    ).execute()

    files = response.get("files", [])
    if not files:
        print("No matching file found in the folder.")
        return None
    
    latest_file = files[0]
    return latest_file["id"]

def download_file(file_id, destination_path, drive_service):
    """
    Downloads a file from Google Drive to the specified local path.

    Args:
        file_id (str): The ID of the Drive file to download.
        destination_path (str): Local path to save the file.
        drive_service (Resource): Authenticated Drive API service.
    """
    request = drive_service.files().get_media(fileId=file_id)
    fh = FileIO(destination_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download progress: {int(status.progress() * 100)}%")
    
    print(f"File downloaded to {destination_path}")
