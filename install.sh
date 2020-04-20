#!/bin/bash

set -e


# Name of the app (can be customised)
APP_NAME='vault'

# Install dirs (can be customised)
LINK_DIR='/usr/local/bin'
FILES_DIR='/opt'

# Colors
RED='\e[31m'
GREEN='\e[32m'
DEF='\e[0m'


# install python 3.7
sudo apt-get install python3

#insstall pip3
sudo apt-get install python3-pip

#install necessary python libraries
pip3 install -U google-api-python-client google-auth-httplib2 google-auth-oauthlib

# create credential folder
mkdir -p ~/.CREDENTIAL_FILES

# copy all the necessary files
sudo mkdir -p $FILES_DIR
sudo cp -ar ./Backup_client $FILES_DIR'/'
chmod u+x $FILES_DIR/Backup_client/backup_client.py

#create a soft link to the backup_client
sudo ln -s  $FILES_DIR'/Backup_client/backup_client.py' $LINK_DIR'/'$APP_NAME

echo -e $GREEN'Installation finished successfully'$DEF
