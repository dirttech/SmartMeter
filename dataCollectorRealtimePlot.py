#!/usr/bin/env python

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusSocketFramer as ModbusFramer
import csv
import datetime
import time
from Utilities import convert, makeFolder, delete_older_folders,find_tty_usb
from ConfigurationL import METER_PORT, METER_ID, DATA_BASE_PATH, THRESHOLD_TIME, \
    TIMEZONE, BAUD_RATE, HEADER ,DEVICE_ID, \
	STOP_BITS,BYTE_SIZE,PARITY,COM_METHOD,TIME_OUT,BASE_REGISTER,BLOCK_SIZE, RETRIES, ID_VENDOR, ID_PRODUCT
import subprocess
import sys
from gevent_zeromq import zmq
from geventwebsocket.handler import WebSocketHandler
import gevent
import json
import paste.urlparser
import pytz
import os

def CONNECT_TO_METER():

    try:
        client = None
        METER_PORT = find_tty_usb(ID_VENDOR, ID_PRODUCT)        #reading to which port rs485(client) is connected
        client = ModbusClient(retries = RETRIES, method=COM_METHOD, port=METER_PORT, baudrate=BAUD_RATE, stopbits=STOP_BITS, parity=PARITY, bytesize=BYTE_SIZE, timeout=TIME_OUT)
        client.connect()
        return client

    except Exception as e:
        print "Could not connect to client: \n" + e.__str__()
        log_file=open(DATA_BASE_PATH+"RealtimeLOG.txt","a")
        log_file.write(str(time.time())+" Could not connect to client: \n"+e.__str__()+"\n")
        log_file.close()

global start_time
start_time=int(time.time())

global now
now = datetime.datetime.now()

global start_day
start_day=now.day

global start_month
start_month=now.month


def READ_METER_DATA (regIndex, numRegisters, slaveUnit, client):			#Function for reading meter data
    result = client.read_holding_registers(regIndex, numRegisters, unit=slaveUnit)
    return result

def main():
    
    '''Set up zmq context and greenlets for all the servers, then launch the web browser and run the data producer'''
    context = zmq.Context()
    
    # zeromq: tcp to inproc gateway
    gevent.spawn(zmq_server, context)
    
    ws_server = gevent.pywsgi.WSGIServer(('', 9999), WebSocketApp(context),handler_class=WebSocketHandler)
    # http server: serves up static files
    http_server = gevent.pywsgi.WSGIServer(('', 8000),paste.urlparser.StaticURLParser(os.path.dirname(__file__)))
 
    client = CONNECT_TO_METER()
    
    # Start the server greenlets
    http_server.start()
    ws_server.start()	
        
    global count
    count=0
    makeFolder(start_day, start_month)
            
    f =open(DATA_BASE_PATH +str(start_day)+"_"+str(start_month)+"/"+str(count)+".csv","a")
    f.write(HEADER)
    f.close()

    zmq_producer(context, client)


def zmq_server(context):
    '''Funnel messages coming from the external tcp socket to an inproc socket'''
       
    sock_incoming = context.socket(zmq.SUB)
    sock_outgoing = context.socket(zmq.PUB)
    
    sock_incoming.bind('tcp://*:5000')
    sock_outgoing.bind('inproc://queue')
    sock_incoming.setsockopt(zmq.SUBSCRIBE, "")
    while True:
        msg = sock_incoming.recv()
        sock_outgoing.send(msg)

class WebSocketApp(object):
    '''Funnel messages coming from an inproc zmq socket to the websocket'''

    def __init__(self, context):
        self.context = context

    def __call__(self, environ, start_response):
        ws = environ['wsgi.websocket']
        sock = self.context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect('inproc://queue')
        while True:
            msg = sock.recv()
            ws.send(msg)

def zmq_producer(context, client):
    socket = context.socket(zmq.PUB)
    socket.connect('tcp://127.0.0.1:5000')

    while True:
	          
        now_time=int(time.time())
        now = datetime.datetime.now()
        now_day=now.day
        now_month=now.month
       	
	global start_time, start_day, count
        if ((now_time-start_time) > THRESHOLD_TIME) or (now_day!=start_day):
                        
            count = count + 1
	    makeFolder(now_day, now_month)                   
	    delete_older_folders(now)
            f =open(DATA_BASE_PATH +str(now_day)+"_"+str(now_month)+"/"+str(count-1)+".csv","a")
            f.write(HEADER)
            f.close()          
            
            start_time=now_time
            start_day=now_day
            start_month=now_month
                    
        else:
                              
            for mId in range (0,len(METER_ID)): 
                                    
                try:
                    MID=METER_ID[mId]		    

                    r1=int(time.time())
                    row = str(DEVICE_ID)+","+str(MID)+","+str(r1)#Writing time and other variables in row
                    
                    k = READ_METER_DATA(BASE_REGISTER,BLOCK_SIZE, MID, client)			      #Calling function to read meter                
                    
                    for i in range (0,(BLOCK_SIZE-1),2):
                        
                                                    
                        kt= (k.registers[i+1]<<16) + k.registers[i]			      #Formating & Filtering collected data / making it suitable for CSV format
                        kkt =","+ str(convert(kt))
                        row = row +kkt                      
                               
                   
                    print "Meter: "+str(MID) +"\n"+str(row)

                    row=row[:-1]+"\n"
                    
                    global start_day, start_month
                    
                    makeFolder(start_day,start_month)
                    
                    socket.send(row)            #sending meter data (row) to socket for live visualization
                    
                    f =open(DATA_BASE_PATH +str(start_day)+"_"+str(start_month)+"/"+str(count)+".csv","a")
                    
                    f.write(row)		#writing meter data (row) in CSV
                    
                    gevent.sleep(0.05)		#never remove this delay / you may change amount of delay
                    
                    f.close()
                                
                except Exception as e:
                    print "Meter: "+str(MID)+" \n" + e.__str__()
                    log_file=open(DATA_BASE_PATH+"Meter_"+str(MID)+"Meterlog.txt","a")
                    log_file.write(str(time.time())+" "+e.__str__()+"\n")
                    log_file.close()
                                        
                    client = None
                    client = CONNECT_TO_METER()



if __name__ == '__main__':
    main()
