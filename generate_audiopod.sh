#!/bin/bash

# 0. Bring in files to /files, rename m4b to m4a
# 1. Create ngrok tunnel 
# 2. Pass in public ip for ngrok tunnel to python script to generate xml
# 3. Upload in Overcast
echo "Hello from shell script"
env/bin/python audiopod.py http://3895cb99.ngrok.io
export FLASK_APP=audiopod.py
flask run
