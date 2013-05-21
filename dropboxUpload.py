#!/usr/bin/env python
 
#You have to add app_secret , app_key , username and password for your dropbox acc and dropbox app before using it. Not a plug and play

from dropbox import client, rest, session
import mechanize
import glob
import os
import time
from ConfigurationZ import DATA_BASE_PATH, THRESHOLD_TIME, DEVICE_ID
import datetime
import shutil
from UtilitiesZ import list_subdirectories
       

try:
    list_dir = list_subdirectories(DATA_BASE_PATH)

    br = mechanize.Browser()
    br.set_handle_robots(False)

    #login into dropbox
    br.open('https://www.dropbox.com/login')
    isLoginForm = lambda f: f.action == "https://www.dropbox.com/login" and f.method == "POST"
    br.select_form(predicate=isLoginForm)
    br['login_email'] = 'your mail @gmail.com'
    br['login_password'] = 'password'
    response = br.submit()

    print 'login done'
    #opening authorization form
    APP_KEY = 'your app key'
    APP_SECRET = 'your app secret'
    ACCESS_TYPE = 'app_folder'

    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

    request_token=sess.obtain_request_token()

    url = sess.build_authorize_url(request_token)
    print "url:", url
    br.open(url)
    br.select_form(nr=1)
    response=br.submit()


    # This will fail if the user didn't visit the above URL and hit 'Allow'
    access_token = sess.obtain_access_token(request_token)

    client1 = client.DropboxClient(sess)
    #print "linked account:", client1.account_info()
    
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

                    f = open(f)
                    
                    response = client1.put_file(DATA_PATH+f1, f)
                    
                    print "upload "+DATA_PATH+f1
                    
                    print "Upload Success. \n Now removing file: "+f1
                        
                    lo=open(DATA_BASE_PATH+"LOG_DROPBOX_UPLOAD.txt","a")
                    lo.write(str(time.time())+"  "+"upload success \n")
                    lo.close()
                                          
                        
            except Exception as f:
                lo=open(DATA_BASE_PATH+"LOG_DROPBOX_UPLOAD.txt","a")
                lo.write(str(time.time())+"  "+"filename: "+f +"  Error: "+f.__str__()+"\n")
                lo.close()
    
                
except Exception as e:
    lo=open(DATA_BASE_PATH+"LOG_DROPBOX_UPLOAD.txt","a")
    lo.write(str(time.time())+"  "+e.__str__()+"\n")
    lo.close()
