#!/usr/bin/env bash

echo username:password | sudo chpasswd
sudo apt-get install vim-runtime vim tcpdump traceroute snmp-mibs-downloader snmpd nmap snmp mtr dnsutils -y

sudo swapoff --all
sudo update-rc.d -f dphys-swapfile remove
sudo rm -f /var/swap
sudo apt-get --purge autoremove dphys-swapfile -y

sudo sh -c 'echo PI-`cat /proc/cpuinfo | grep Serial | cut -d" " -f2` >/etc/hostname'
sudo sysctl kernel.hostname=`cat /etc/hostname`
grep -Fx "127.0.0.1       `cat /etc/hostname`" /etc/hosts || sudo sh -c 'echo "127.0.0.1       `cat /etc/hostname`" >> /etc/hosts'

grep -Fx "gpu_mem=256" /boot/config.txt || sudo sh -c 'echo "gpu_mem=256" >> /boot/config.txt'

sudo apt-get remove --purge wolfram-engine scratch nuscratch sonic-pi idle3 smartsim java-common minecraft-pi python-minecraftpi python3-minecraftpi

mkdir /home/pi/.config/autostart
FILE=/home/pi/.config/autostart/kiosk.desktop

if [ ! -e "$FILE" ]
then
  cat <<EOT >> "$FILE"
[Desktop Entry]
Type=Application
Name=Kiosk
Exec=/home/pi/kiosk.sh
X-GNOME-Autostart-enabled=true
EOT
fi

sudo cp gdrive-linux-rpi /usr/loca/bin/gdrive
sudo cp gdrive-linux-rpi /usr/loca/sbin/gdrive

sudo chmod +x /usr/local/bin/gdrive /usr/local/sbin/gdrive


# click on that url
# copy and past the url that the first url shows into the console
