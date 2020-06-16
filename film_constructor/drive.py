from google.oauth2 import service_account
from googleapiclient.discovery import build

from json import dumps
from os import environ

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'


class Drive:
    def __init__(self):
        # Getting environment variables
        self.project_id = environ.get('project_id')
        self.private_key_id = environ.get('private_key_id')
        self.private_key = environ.get('private_key')
        self.client_email = environ.get('client_email')
        self.client_id = environ.get('client_id')
        self.client_x509_cert_url = environ.get('client_x509_cert_url')

        # Initializing driver
        self.create_creds_file()
        self.init_creds()
        self.drv = build('drive', 'v3', credentials=self.creds)

        # Check folders
        folders = self.drv.files().list(q="mimeType = 'application/vnd.google-apps.folder'").execute()
        if folders:
            for folder in folders['files']:
                if folder['name'] == self.default_folder:
                    self.default_folder_id = folder.get('id')
                    return

        self.default_folder_id = self.create_folder(self.default_folder)
        self.add_reader_permission(self.default_folder_id)

    def init_creds(self):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES)
        self.creds = creds

    def create_creds_file(self):
        # Service account credentials template
        file_dump = {
            "type": "service_account",
            "project_id": self.project_id,
            "private_key_id": self.private_key_id,
            "private_key": self.private_key,
            "client_email": self.client_email,
            "client_id": self.client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": self.client_x509_cert_url
        }

        with open(SERVICE_ACCOUNT_FILE, 'w') as f:
            f.write(dumps(file_dump))

    def create_folder(self, name: str):
        """
        Creates folder on drive and returning it's id.
        :param name: Name of new folder
        :return: Folder id
        """
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.drv.files().create(body=file_metadata,
                                         fields='id').execute()
        return folder.get('id')

    def add_reader_permission(self, file_id):
        metadata = {
            "role": "reader",
            "type": "anyone"
        }
        return self.drv.permissions().create(fileId=file_id, body=metadata).execute()

    def add_file(self, filename: str, folder_id: str = None, title: str = None):
        """
        Add file to drive.
        :param filename: Path to file for upload
        :param folder_id: Id of folder parent
        :param title: Name of file on drive
        :return: Google-drive file object (Not python file-object)
        """
        if folder_id is None:
            folder_id = self.default_folder_id

        if title is None:
            title = filename

        metadata = {'title': title,
                    'name': title,
                    'uploadType': 'media',
                    'parents': [folder_id]}
        file = self.drv.files().create(body=metadata, media_body=filename, fields='webContentLink').execute()
        return file

    def get_file(self, file_id: str, fields: str = None):
        """
        Return file from drive
        :param file_id: Id of file to get
        :param fields: Additional fields to get from file
        :return:
        """
        return self.drv.files().get(fileId=file_id, fields=fields).execute()

    creds = None
    drv = None
    default_folder = 'drive'
    default_folder_id = None
