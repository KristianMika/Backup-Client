# Backup-Client


Backup client is a simple client, that uses Google Drive Api and is able to upload / download your files from google drive.
All files (even their names) are encrypted before being uploaded to your drive account.



## Requirements
```
python 3.7
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```


## Quick start

- [Enable](https://developers.google.com/drive/api/v3/quickstart/js) the drive API in your drive account.
- Download "credentials.json" file an save it to CREDENTIAL_FOLDER.
- Run [installation script](./install.sh)

## Usage
```
 vault [-h] [-v] [-f] [-o OUTPUT] action [action_arg]
 
 positional arguments:
  action                UPLOAD / DOWNLOAD
  action_arg            [file name]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         enable verbose mode
  -f, --force           overwrite files without asking
  -o OUTPUT, --output OUTPUT
                        selects output path

```
![demo gif](./images/demo.gif)

#### Disclaimer!!!
##### This is just a simple weekend project and is not intended to be used in a real life.