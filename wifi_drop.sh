#!/bin/bash

while true ; do
   if ifconfig wlan0 | grep -q "inet addr:" ; then
      sleep 60
   else
      echo "Network connection down! Attempting reconnection."
      ifdown --force wlan0
      sleep 10
      ifup --force wlan0
      sleep 10
    fi
done
