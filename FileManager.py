import io

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import util


class FileManager:
    def list_files(self, service):
        # results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        results = service.files().list().execute()
        items = results.get('files', [])
        util.prettify_listing(items)

    def upload(self, file_path, service):
        file_name = util.get_file_name(file_path)
        print("Uploading {}...".format(file_name))
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path)
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
        print("Finished...\n")

    def download(self, service, id):
        request = service.files().get_media(fileId=id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        util.save_file(fh)
        print()

    def create_folder(self, service, directory):
        file_metadata = {
            'name': directory,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = service.files().create(body=file_metadata,
                                      fields='id').execute()

    def search_file(self, service, file_name):
        results = service.files().list(q="name contains '" + file_name + "'").execute()
        items = results.get('files', [])
        # util.prettify_listing(items)
        return items[0]["id"]
