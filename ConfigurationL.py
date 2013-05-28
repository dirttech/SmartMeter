#!/usr/bin/env python

import os
import sys


THRESHOLD_TIME=900                    #Time in seconds after which a new CSV gets created

CODE_PATH = os.path.dirname(sys.argv[0])

DATA_BASE_PATH=CODE_PATH + "/Meter_Data/" #The path where the data gets stored

ID_VENDOR = '0403'
ID_PRODUCT = '6001'

METER_ID=[1,2,3,4] 		      #The slave id assigned to the meter

GMT_TIME_DIFFERENCE_MILLISECONDS=19800000

BASE_UPLOAD_PATH=""

TIMEZONE='Asia/Kolkata'

HEADER="Building_Id,Floor_Id,Wing_Id,Meter_Id,Timestamp,VA,W,VAR,PF,VLL,VLN,A,F,VA1,W1,VAR1,PF1,V12,V1,A1,VA2,W2,VAR2,PF2,V23,V2,A2,VA3,W3,VAR3,PF3,V31,V3,A3,FwdVAh,FwdWh,FwdVARh(inductive),FwdVARh(capacitive)\n"

BUILDING_ID = 1
FLOOR_ID = 1
WING_ID = 1

#-------Modbus Variables-----------------------------------

STOP_BITS = 1
BYTE_SIZE = 8
PARITY = 'N'
COM_METHOD = 'rtu'
TIME_OUT = 0.1
BAUD_RATE=19200                   #The baud rate for serial communication

BASE_REGISTER = 3900
BLOCK_SIZE = 66
RETRIES = 3
