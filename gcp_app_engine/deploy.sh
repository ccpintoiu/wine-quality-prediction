#!/bin/bash

#cd application
pip install -r requirements.txt -t lib
# uncomment below for initial app creation
#gcloud app create
#gcloud app deploy
gcloud app deploy --project data-engineering-229511 -v 20190520t195634
PROJECT=data-engineering-229511

PROJECT=data-engineering-229511
echo "Visit https://PROJECT-ID.appspot.com/  e.g. https://${PROJECT}.appspot.com"
echo "https://data-engineering-229511.appspot.com"
