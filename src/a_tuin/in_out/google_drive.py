__copyright__ = 'Copyright(c) Gordon Elliott 2020'

""" Utilities to manipulate Google Drive
"""

import io
import logging
import os
import importlib_resources

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

LOG = logging.getLogger(__file__)

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
PDF_MIME_TYPE = 'application/pdf'


def get_credentials_path(configuration):
    ref = importlib_resources.files(configuration.folders.root_package) / os.path.join(configuration.folders.config, configuration.gdrive.credentials_file)
    return ref


def get_gsuite_service(configuration, service_name, service_version):
    credentials_path = get_credentials_path(configuration)
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    scoped_credentials = credentials.with_scopes(SCOPES)
    return build(service_name, service_version, credentials=scoped_credentials, cache_discovery=False)


def get_gdrive_service(configuration):
    return get_gsuite_service(configuration, 'drive', 'v3')


def get_gdocs_service(configuration):
    return get_gsuite_service(configuration, 'docs', 'v1')


def files_in_folder(service, query, page_size=100):
    child_files = service.files().list(
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
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
    return buffer


def download_textfile(request):
    buffer = download(request)
    wrapper = io.TextIOWrapper(buffer, encoding='utf-8')
    wrapper.seek(0)     # this is essential in order that the CSV contents can be read
    return wrapper


def download_as_pdf(service, merged_file_id, out_file_name):
    request = service.files().export_media(fileId=merged_file_id, mimeType=PDF_MIME_TYPE)
    buffer = download(request)
    with open(out_file_name, 'wb') as outfile:
        outfile.write(buffer.getvalue())


def upload_to_gdrive(gdrive, source_file_path, name_for_uploaded_file, mime_type, share_with_email):
    media = MediaFileUpload(source_file_path, mimetype=mime_type)
    uploaded_file_id = gdrive.files().create(
        body={'name': name_for_uploaded_file},
        media_body=media,
        fields='id'
    ).execute().get('id')
    permissions = {
        "role": "writer",
        "type": "user",
        "emailAddress": share_with_email
    }
    gdrive.permissions().create(body=permissions, fileId=uploaded_file_id).execute()
    return uploaded_file_id
