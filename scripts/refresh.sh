#!/usr/bin/env bash
#rm /home/pi/CH/*
#logger "removed all images from ~/CH/ directory"
#rm /home/pi/html/*
#logger "removed all html pages from ~/html/"

mkdir -p /home/pi/html
logger "Creating html directory if it does not exist"

id=`/usr/local/sbin/gdrive list | grep CH | awk '{print $1 }'`
echo "id of the content directory is "$id""
logger "id is "$id""
/usr/local/sbin/gdrive download "$id" --recursive --force >> /home/pi/log.log
logger "pulled content from google drive"

logger "verifying images"
logger ls -d /home/pi/CH/*

python3 /home/pi/generate-html-pages.py

logger "verifying html pages"
logger ls -d /home/pi/html/*


#logger "killing chromium"

#ppid=`ps aux | grep /home/pi/kiosk.sh | head -1 | awk '{print $2}'`

#kill -9 "$ppid"

#logger "starting chromium"
#cd /home/pi
#source "/home/pi/kiosk.sh" &
