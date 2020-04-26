__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" 
"""

import io
import logging
import pkg_resources

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


LOG = logging.getLogger(__file__)

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]


def get_credentials_path(module_name, gdrive_config):
    return pkg_resources.resource_filename(
        module_name,
        '../config/{}'.format(gdrive_config.credentials_file)
    )


def get_gdrive_service(module_name, drive_config):
    credentials_path = get_credentials_path(module_name, drive_config)
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    scoped_credentials = credentials.with_scopes(SCOPES)
    return build('drive', 'v3', credentials=scoped_credentials, cache_discovery=False)


def files_in_folder(service, query, page_size=100):
    child_files = service.files().list(
        q=query,
        pageSize=page_size,
        fields="nextPageToken, files(id, name)"
    ).execute()
    LOG.debug(child_files)
    for file_in_folder in child_files['files']:
        yield file_in_folder['id'], file_in_folder['name']


def download(request):
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if status:
            LOG.debug(f"Download {int(status.progress() * 100)}")
    wrapper = io.TextIOWrapper(buffer, encoding='utf-8')
    wrapper.seek(0)     # this is essential in order that the CSV contents can be read
    return wrapper
