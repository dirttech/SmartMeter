#!/usr/bin/env python

import requests
import glob
import os
import time
from ConfigurationZ import DATA_BASE_PATH, THRESHOLD_TIME, DEVICE_ID
import datetime
import shutil
from UtilitiesZ import list_subdirectories
import datetime            

try:
    list_dir = list_subdirectories(DATA_BASE_PATH)
    
    for d in list_dir:
        
        DATA_PATH =DATA_BASE_PATH+d+"/"
        print "Entering: "+DATA_PATH
        list_of_files=glob.glob(DATA_PATH+str("/*.csv"))
        for f in list_of_files:
            try:
                print "Entering: "+f            
                if int(time.time())-int(os.stat(f).st_mtime)>THRESHOLD_TIME:
                
                    head, tail = os.path.split(f)
                               
                    f1 = "D"+str(DEVICE_ID)+"_C"+tail
                    
                    os.rename(f,DATA_PATH+f1)  
                              
                    files = {'Data': open(DATA_PATH+f1, 'rb')}
                    print "upload "+DATA_PATH+f1
                    r = requests.post(url='http://sensoract.iiitd.edu.in:9006',files=files)
                    
                    if r.status_code==200:
                        print "Upload Success. \n Now removing file: "+f1
                        os.remove(DATA_PATH+f1)
                        
                        lo=open(DATA_BASE_PATH+"LOG_UPLOAD.txt","a")
                        lo.write(str(time.time())+"  Removed: "+DATA_PATH+f1+"upload success \n")
                        lo.close()
                    else:
                        os.rename(DATA_PATH+f1,f)                        
                        
            except Exception as e:
                lo=open(DATA_BASE_PATH+"LOG_UPLOAD.txt","a")
                lo.write(str(time.time())+"  "+"filename: "+f +"  Error: "+e.__str__()+"\n")
                lo.close()
    
                
except Exception as e:
    lo=open(DATA_BASE_PATH+"LOG_UPLOAD.txt","a")
    lo.write(str(time.time())+"  "+e.__str__()+"\n")
    lo.close()
