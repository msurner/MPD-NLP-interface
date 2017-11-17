#!/bin/bash
PORT=5000

if [ $# -eq 0 ]
  then
    echo "Usage: $0 \"Message to send\""
    exit
fi

curl -X GET http://localhost:$PORT/`echo $1 | sed -e "s/ /%20/g"`
