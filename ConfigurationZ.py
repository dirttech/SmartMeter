#!/usr/bin/env python

import os
import sys  

THRESHOLD_TIME=900                    #Time in seconds after which a new CSV gets created

CODE_PATH = os.path.dirname(sys.argv[0])

DATA_BASE_PATH = CODE_PATH + "/Meter_Data/"   #The path where the data gets stored

LOG_PATH = CODE_PATH+"/"

ID_VENDOR = '0403'
ID_PRODUCT = '6001'

METER_ID=[1,2,3,4] 		      #The slave id assigned to the meter

HEADER="Timestamp,A1,A2,A3,V1,V2,V3,PF1,PF2,PF3,F,Onhrs,FwdWh,RevWh\n"

BASE_UPLOAD_PATH=""

GMT_TIME_DIFFERENCE_MILLISECONDS=19800000

TIMEZONE='Asia/Kolkata'

HEADER="DeviceID,MeterID,Timestamp,W,F,PF1,V1,A1,PF2,A2,PF3,A3,FwdWh\n"

POSITION_HEADER=[2,14,22,26,28,36,42,50,56,60]

DEVICE_ID = 1       #Raspberry pi ID


#-------Modbus Variables-----------------------------------

STOP_BITS = 1
BYTE_SIZE = 8
PARITY = 'N'
COM_METHOD = 'rtu'
TIME_OUT = 0.1
BAUD_RATE=19200                   #The baud rate for serial communication

BASE_REGISTER = 3900
BLOCK_SIZE = 66
RETRIES = 2
