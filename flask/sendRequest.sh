#!/bin/bash
PORT=5000

if [ $# -eq 0 ]
  then
    echo "Usage: $0 \"Message to send\" {userid}"
    exit
fi

USERID=1
if [ $# -eq 2 ]
  then
    USERID=$2
fi

# Set output color to cyan
CYAN='\033[1;36m'
echo -e "${CYAN}"

curl -X GET http://localhost:$PORT/?userid=$USERID\&input=`echo $1 | sed -e "s/ /%20/g"`

echo ""
