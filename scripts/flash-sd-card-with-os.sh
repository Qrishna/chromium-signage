#!/usr/bin/env bash

# A script that flashes an image to a volume
# It is intended to be used on Mac OS X only

# $1 = full path of the image
# $2 = disk identifier
# $3 = file system format
# $4 = block size
# $5 = name for the 'to be' newly formatted volume

# If these arguments are not supplied the script will use the defaults defined below

DEFAULT_IMAGE=~/Downloads/2016-05-27-raspbian-jessie-lite.img           # Set default image
DEFAULT_DISK_IDENTIFIER="/dev/rdisk2"                                   # Set default disk identifier use rdisk2 for speed
DEFAULT_FILE_SYSTEM_FORMAT="fat32"                                      # Set fat32 as the default file format

DEFAULT_BLOCK_SIZE=4m                                                   # Set default block size to 4MB
DEFAULT_DISK_IDENTIFIER_NAME="PI"                                       # Set PI as the default name for the newly formatted volume

ROOTUSER_NAME=root                                                      # Script must be run by root
STATUS_NOTROOT=81
STATUS_NOIMAGE=82

username=$(id -nu)
if [ "$username" != "$ROOTUSER_NAME" ]
then
  echo "The script needs to be run with root privileges"
  exit $STATUS_NOTROOT
fi

if [ -n "$1" ]
then
  image="$1"
else
  image="$DEFAULT_IMAGE"
fi

if [ -n "$2" ]
then
  volume="$2"
else
  volume="$DEFAULT_DISK_IDENTIFIER"
fi

if [ -n "$3" ]
then
  format="$3"
else
  format="$DEFAULT_FILE_SYSTEM_FORMAT"
fi

if [ -n "$4" ]
then
  block_size="$4"
else
  name="$DEFAULT_BLOCK_SIZE"
fi

if [ -n "$5" ]
then
  name="$5"
else
  name="$DEFAULT_DISK_IDENTIFIER_NAME"
fi

if [ ! -e $image ]
then
  echo "No Image  \"$image\" not found!"
  exit $STATUS_NOIMAGE
fi

echo "Unmounting the volume $volume to prepare for erasing"
diskutil unmountDisk $volume
if [ $? -eq 0 ]; then
  echo "Unmounting the volume $volume was successful."
else
  exit
fi

echo "Erasing the volume $volume as a $format and naming the volume $name"
diskutil eraseDisk $format $name $volume
if [ $? -eq 0 ]; then
  echo "Erasing the volume $volume was successful."
else
  exit
fi

echo "Sleep for 5 seconds"
sleep 5

echo "Unmount the volume $volume one more time"
diskutil unmountDisk $volume
if [ $? -eq 0 ]; then
  echo "Unmounting the volume $volume was successful."
else
  exit
fi

echo "Writing $image to the volume $volume"
dcfldd bs=$block_size if=$image of=$volume
if [ $? -eq 0 ]; then
  echo "Successfully wrote $image to the $volume"
else
  exit
fi

echo "Running sync to flush the write cache"
sudo sync

echo "Ejecting the volume $volume"
diskutil eject $volume

ESTATUS=$?
echo "It is now safe to unplug your disk and it is ready for use!"
exit ESTATUS
