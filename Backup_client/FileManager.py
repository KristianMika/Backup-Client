import io

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import util


class FileManager:
    """ Class that represents a File Manager.

        It's main purpose is to upload, download and list files from the Google Drive """

    def __init__(self, service):
        self.service = service

    def list_files(self):
        """ Lists all files that are currently in the drive and returns them as a list"""

        results = self.service.files().list().execute()
        return results.get('files', [])

    def upload(self, file_path):
        """ Uploads file to the drive """

        file_name = util.get_file_name(file_path)
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    def download(self, id, path, name):
        """ Download a file with it's id == <id> and stores it to path/name """

        request = self.service.files().get_media(fileId=id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Downloading: {}% ...".format(int(status.progress() * 100)))

        util.save_file(fh, path, name)

    def create_folder(self, directory):
        """ Creates a directory in the drive """

        file_metadata = {'name': directory, 'mimeType': 'application/vnd.google-apps.folder'}
        file = self.service.files().create(body=file_metadata, fields='id').execute()

    def search_file(self, f_name):
        """ Searches for a file name in the drive """

        results = self.service.files().list(q="name contains '" + f_name + "'").execute()
        return results.get('files', [])

    def delete(self, item):
        """ Deletes <item> from the drive  """

        del_response = self.service.files().delete(fileId=item['id']).execute()

    def empty_trash(self):
        """ Empties the Google Drive trash
            Currently useless, since all removed files are irretrievable
            TODO: INSTEAD OF REMOVING FILES, MOVE THEM TO THE TRASH """

        trash_response = self.service.files().emptyTrash().execute()
