#!/usr/bin/env bash

id=`/usr/local/sbin/gdrive list | grep CH | awk '{print $1 }'`
echo "id of the content directory is "$id""
logger "id is "$id""
/usr/local/sbin/gdrive download "$id" --recursive --force >> /home/pi/log.log
logger "pulled content from google drive"

logger ls -d /home/pi/CH/*

python3 /home/pi/generate-html-pages.py >> log.log
logger ls -d /home/pi/html/*
function join_by { local IFS="$1"; shift; echo "$*"; }

HTML=../html

#htmlpages=`join_by " " $HTML/**`
htmlpages=`python3 $PWD/listthings.py`
# Run this script in display 0 - the monitor
export DISPLAY=:0

# Hide the mouse from the display
unclutter &

# If Chrome crashes (usually due to rebooting), clear the crash flag so we don't have the annoying warning bar
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

# Run Chromium and open tabs
#/usr/bin/chromium-browser --window-size=480,320 --kiosk --window-position=0,0 www.catapulthealth.com join_by  &
command="/usr/bin/chromium-browser --window-size=480,320 --kiosk --window-position=0,0 --incognito www.catapulthealth.com $htmlpages & > /home/pi/log.log"
logger "Command looks like this:"
logger "$command"
eval $command

# Start the kiosk loop. This keystroke changes the Chromium tab
# To have just anti-idle, use this line instead:
# xdotool keydown ctrl; xdotool keyup ctrl;
# Otherwise, the ctrl+Tab is designed to switch tabs in Chrome
# #
while (true)
  do
    xdotool keydown ctrl+Tab; xdotool keyup ctrl+Tab;
    sleep 10
  done