from __future__ import print_function
import client_auth
import FileManager
import FileCipher


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():

    service = client_auth.authorize()

    man = FileManager.FileManager()

    enc = FileCipher.FileCipher()


    key = enc.generate_bytes(32)
    iv = enc.generate_bytes(16)

    man.list_files(service)



    man.list_files(service)



    ##man.create_folder(service, "tmp")

    #man.search_file(service, "LICENSE")
if __name__ == '__main__':
    main()


    """
    https://developers.google.com/drive/api/v3/search-files
    
    """