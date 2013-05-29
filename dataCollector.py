#!/usr/bin/env python

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusSocketFramer as ModbusFramer
import csv
import datetime
import time
from Utilities import convert, makeFolder, delete_older_folders, find_tty_usb
from ConfigurationZ import METER_ID, DATA_BASE_PATH, THRESHOLD_TIME, \
    TIMEZONE, BAUD_RATE, HEADER ,DEVICE_ID,POSITION_HEADER, \
    STOP_BITS,BYTE_SIZE,PARITY,COM_METHOD,TIME_OUT,BASE_REGISTER,BLOCK_SIZE, RETRIES, LOG_PATH, ID_VENDOR, ID_PRODUCT
import subprocess
import sys
import os
import logging
import logging.handlers
import gc
#import psutil



'''Logging framework starts here'''
lgr = logging.getLogger('SmartMeter App')  #created logger
lgr.setLevel(logging.ERROR)

fh = logging.handlers.RotatingFileHandler(LOG_PATH+"OuterLog.log", maxBytes = (1024*1024*50), backupCount=10) #added file handler
fh.setLevel(logging.WARNING)

frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  #created formatter
fh.setFormatter(frmt) #set formatter for handler

lgr.addHandler(fh)    #added handler to logger
'''Logging framework ends here'''


''' testing Framework starts here'''
class DataCollectorError(Exception) :
    
    def __init__(self, msg=''):
        
        self.msg = msg
        lgr.error('Custom Error: ', self.msg)
        print "Custom Error: \n"+ self.msg
        
    def __str__(self):
        return self.msg
    
    pass

class ParamNullError(DataCollectorError) : pass
class ParamInvalidTypeError(DataCollectorError) : pass
class ParamOutOfRangeError(DataCollectorError) : pass
class ParamInvalidFormatError(DataCollectorError) : pass
class InvalidPathFormatError(DataCollectorError): pass
class PathNotExistsError(DataCollectorError): pass
class FaultyFileError(DataCollectorError): pass

'''testing framework ends here'''


def CONNECT_TO_METER():

    try:
        client = None
        METER_PORT = find_tty_usb(ID_VENDOR, ID_PRODUCT)        #reading to which port rs485(client) is connected
        client = ModbusClient(retries = RETRIES, method=COM_METHOD, port=METER_PORT, baudrate=BAUD_RATE, stopbits=STOP_BITS, parity=PARITY, bytesize=BYTE_SIZE, timeout=TIME_OUT)
        client.connect()
        return client

    except Exception as e:
        lgr.error('Error while connecting client: ', exc_info = True)
        print "Error while connecting client: \n"+e.__str__()



def READ_METER_DATA (regIndex, numRegisters, slaveUnit, client):

    if not regIndex:
        raise ParamNullError, "register index is null"

    if not numRegisters:
        raise ParamNullError, "number of registers should not be null"

    if not slaveUnit:
        raise ParamNullError, "Meter Id should not be null"

    if not isinstance(regIndex, int):
        raise ParamInvalidTypeError, "register index passed is not int"

    if not isinstance(numRegisters, int):
        raise ParamInvalidTypeError, "number of registers passed is not int"

    if not isinstance(slaveUnit, int):
        raise ParamInvalidTypeError, "meter id passed is not int"

    if not 3900 <= regIndex <= 4000:
        raise ParamOutOfRangeError, "Initial register index should be b/w 3900-4000"

    if(regIndex % 2 != 0):
        raise ParamInvalidFormatError, "Initial register index should be even"

    if not 2 <= numRegisters <= 100:
        raise ParamOutOfRangeError, "Number of registers to read should be b/w 2 - 100"

    if (numRegisters % 2 != 0):
        raise ParamInvalidFormatError, "Number of registers to read should be even"

    if not 1 <= slaveUnit <= 31:
        raise ParamOutOfRangeError, "Meter Id passed should be b/w 1 - 31"
    
    try:
                
        result = client.read_holding_registers(regIndex, numRegisters, unit=slaveUnit)
        return result
    
    except:
        lgr.error('Unexpected Error: ', sys.exc_info())
        print 'Unexpected Error: ', sys.exc_info()
        pass
                 
        
        

def FORMAT_READ_DATA(regObject, MID):

    if not regObject:
        raise ParamNullError, "Register object passed is null"

    if not MID:
        raise ParamNullError, "Meter Id passed is null"

    if not isinstance(MID, int):
        raise ParamInvalidTypeError, "Meter id pass is of wrong type (should be int)"

    #if not isinstance(regObject, str):
    #    raise ParamInvalidTypeError, "Register object passed is of wrong type: "+str(type(k))
    try:

        r1=int(time.time())
        row = str(DEVICE_ID)+","+str(MID)+","+str(r1)
        for i in range (0,(BLOCK_SIZE-1),2):
            for j in POSITION_HEADER:
                if(j == i):                            
                    kt= (regObject.registers[i+1]<<16) + regObject.registers[i]     #Formating & Filtering collected data / making it suitable for CSV format
                    kkt =","+ str(convert(kt))
                    row = row +kkt
                   
        row=row[:-1]+"\n"
        return row

    except:
        lgr.error('Unexpected Error: FORMAT_READ_DATA', sys.exc_info())
        print 'Unexpected Error: FORMAT_READ_DATA', sys.exc_info()
        pass
    
def WRITING_HEADER(filePath, fileName):

    if not filePath:
        raise ParamNullError, "path should not be empty"
    
    if not fileName:
        raise ParamNullError, "file name should not be empty"

    if not isinstance(filePath, str):
        raise ParamInvalidTypeError, "file path should be string type"
    
    if not isinstance(fileName, str):
        raise ParamInvalidTypeError, "file name should be string type"

    if not os.path.exists(filePath):
        raise PathNotExistsError, "path does not exists"
    
    if (fileName.endswith(".csv") == False):
        raise FaultyFileError, "file should be .csv"
        
    try:

        f =open(str(filePath)+str(fileName) ,"a")                      #Creating new file
        f.write(HEADER)
        f.close()

    except:
        lgr.error('Unexpected Error: ', sys.exc_info())
        print 'Unexpected Error: ', sys.exc_info()
        pass

             

def WRITE_METER_DATA(filePath, fileName, row):

    if not filePath:
        raise ParamNullError, "path should not be empty"
    
    if not fileName:
        raise ParamNullError, "file name should not be empty"
    
    if not isinstance(filePath, str):
        raise ParamInvalidTypeError, "file path should be string type"
    
    if not isinstance(fileName, str):
        raise ParamInvalidTypeError, "file name should be string type"

    if not os.path.exists(filePath):
        raise PathNotExistsError, "path does not exists"
    
    if (fileName.endswith(".csv") == False):
        raise FaultyFileError, "file should be .csv"

    if (row.endswith('\n') == False):
        raise ParamInvalidFormatError, "row to be dumped should end with \n (new line chr)"
        
    try:

        f =open(filePath+fileName ,"a")   #Writing row into suitable CSV
        f.write(row)
        f.close()

    except:
        lgr.error('Unexpected Error: ', sys.exc_info())
        print 'Unexpected Error: ', sys.exc_info()
        pass

def main():   
        
    try:
        count = 0
        
        start_time=int(time.time())
        now = datetime.datetime.now()
        start_day=now.day
        start_month=now.month

        client = CONNECT_TO_METER()                      #Making connection with rs485 returns client

        makeFolder(now.day,now.month)           #Making folder of todays day_month      

        WRITING_HEADER(DATA_BASE_PATH +str(start_day)+"_"+str(start_month)+"/", str(count)+".csv")

        
        while True:
            gc.collect()            #garbage collection                  
            now_time=int(time.time())
            now = datetime.datetime.now()
            now_day=now.day
            now_month=now.month

            if ((now_time-start_time) > THRESHOLD_TIME) or (now_day!=start_day):

                '''cpuTime = psutil.cpu_times()
                cpuPercent = psutil.cpu_times_percent()
                virtualMemory = psutil.virtual_memory()
                swapMemory = psutil.swap_memory()
                network = psutil.network_io_counters(pernic=True)
                test = psutil.test()

                lgr.critical(cpuTime)
                lgr.critical(cpuPercent)
                lgr.critical(virtualMemory)
                lgr.critical(swapMemory)
                lgr.critical(network)
                lgr.critical(test)'''
                
                count = count + 1
                makeFolder(now_day,now_month)       

                WRITING_HEADER(DATA_BASE_PATH +str(now_day)+"_"+str(now_month)+"/", str(count)+".csv")  #Creating new file after Threshold Limit passed          

                delete_older_folders(now)           #Delete folders older than 2 days       

                start_time=now_time             #Modifying start time to now time
                start_day=now_day
                start_month=now_month
                lgr.critical("New CSV added")
                
            else:

                
                                              
                for mId in range (0,len(METER_ID)):
                                                        
                    try:
                        
                        #Function to read meter data  
                        regObject = READ_METER_DATA(BASE_REGISTER,BLOCK_SIZE, METER_ID[mId], client)
                        
                        rowData = FORMAT_READ_DATA(regObject  , METER_ID[mId])                                    #Function returning formatted data to be put in CSV
                        
                        makeFolder(start_day,start_month)
                       
                        print "Writing :"+"\n"+str(rowData)+"\n"
                
                        WRITE_METER_DATA(DATA_BASE_PATH +str(start_day)+"_"+str(start_month)+"/", str(count)+".csv", rowData)   #Writing row into suitable CSV

                        print "Going Well!"  
                                    
                    except Exception as e:
                        lgr.critical('Internal Exception: Meter: '+str(METER_ID(mId))+'\n', exc_info = True)
                        print "Internal Exception: Meter: "+str(METER_ID(mId))+'\n'+e.__str__()
                        
                        client = None
                        client = CONNECT_TO_METER()

                       
    except Exception as e:
        
        lgr.error('Some how program is terminated', exc_info = True)
        print "Error in outer shell - \n"+e.__str__()
        
        client = None
        client = CONNECT_TO_METER()


if __name__ == "__main__":
    main()

