#!/bin/sh

# cron script for checking wlan connectivity
IP_FOR_TEST="192.168.1.48"
PING_COUNT=1

PING="/bin/ping"

INTERFACE="eth0"

FFLAG="/opt/check_lan/stuck.fflg"

# ping test
$PING -c $PING_COUNT $IP_FOR_TEST > /dev/null 2> /dev/null
if [ $? -ge 1 ]
then
    logger "check_lan: $INTERFACE is down"

touch $FFLAG
date >> $FFLAG
echo 08 > /sys/devices/platform/bcm2708_usb/regoffset
cat /sys/devices/platform/bcm2708_usb/regvalue >> $FFLAG

echo 0x31 > /sys/devices/platform/bcm2708_usb/regvalue
cat /sys/devices/platform/bcm2708_usb/regvalue >> $FFLAG

else
    logger "check_lan: $INTERFACE is up"
#    rm -f $FFLAG 2>/dev/null
fi
