#!/bin/bash

#cd application
pip install -r requirements.txt -t lib
gcloud app create
gcloud app deploy

PROJECT=data-engineering-229511
echo "Visit https://PROJECT-ID.appspot.com/  e.g. https://${PROJECT}.appspot.com"
echo "https://data-engineering-229511.appspot.com"
