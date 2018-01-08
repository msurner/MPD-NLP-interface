#!/bin/bash
if [ $# -eq 0 ]
  then
    echo "Usage: $0 application.py"
    exit
fi

FLASK_APP=$1 python3 -m flask run
