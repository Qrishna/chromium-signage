#chromium-signage


A culmination of scripts/hackery to just make things work. This is in no way form or fashion in a reproducible/redeployable state

```angular2html
$ sudo killall kiosk.sh && sudo service lightdm restart
$ sudo killall chromium-browser
$ sudo killall kiosk.sh
$ */2 * * * * cd /home/pi && kiosk.sh >> log.log 2>&1
```
