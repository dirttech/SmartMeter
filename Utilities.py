from ConfigurationZ import DATA_BASE_PATH
import datetime
import glob
import os
import re
from shutil import copyfile
import struct
import shutil
import time
from os.path import join

re_pattern=re.compile('.*/(\d+)\.csv')


def delete_older_folders(now):
    '''Function to delete a folder older than 2 days'''
    
    two_days_before=now-datetime.timedelta(days=2)
    two_days_before_day=two_days_before.day
    two_days_before_month=two_days_before.month
    path=DATA_BASE_PATH+str(two_days_before_day)+"_"+str(two_days_before_month)
    print "Entering "+path
    if os.path.exists(path):
        list_of_files=glob.glob(path+str("/*.csv"))
        
        if len(list_of_files)==0: #All data has been uploaded, we can now safely delete older folder
            print "Removing "+path
            shutil.rmtree(path)

def convert(s):
    '''Function to convert data into float'''
    return struct.unpack("<f",struct.pack("<I",s))[0]

def makeFolder(now_day,now_month):
    #function to copy files to some location and renaming with certain name
    
    path=DATA_BASE_PATH+str(now_day)+"_"+str(now_month)
    if not os.path.exists(path):
        os.makedirs(path)
        #copyfile(pth+fil1,path+fil1)
	#os.rename(pth+fil1,path+"/"+ren)
	return 0


def find_count(day,month):
    '''Function to correct number of next data file to be generated and create corresponding folders according to date'''
    try:
        path=DATA_BASE_PATH+str(day)+"_"+str(month)

        if not os.path.exists(path):
            os.makedirs(path)
	
            return 0
        else:
            list_of_files=glob.glob(path+str("/*.csv"))
            lt= len(list_of_files)
            if lt == 0:
	        return 0
            else:
	    #print "now in else"
	    #file_numbers_list=len(glob.glob1(path,"
                file_numbers_list=[int(re_pattern.match(file_name).group(1)) for file_name in list_of_files]
                return max(file_numbers_list)+1

    except Exception as e:
        print "error in find_count(): "+e.__str__()
        log_file = open(DATA_BASE_PATH+"UtilitiesLog.txt","a")
        log_file.write(str(time.time())+" error in find_count(): "+e.__str__()+"\n")
        log_file.close()

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def list_subdirectories(path):
    
    try:
        lst = get_immediate_subdirectories(path)
        #print lst
        return lst

    except Exception as e:
        print "error in list subdirs(): "+e.__str__()
        log_file=open(path+"UtilitiesLog.txt","a")
        log_file.write(str(time.time())+" error in list_subdir(): "+e.__str__()+"\n")
        log_file.close()

def count_files(path):

    try:
        list_of_files=glob.glob(path+str("/*.csv"))
        lt=len(list_of_files)
        return lt

    except Exception as e:
        print "error in count_files(): "+e.__str__()
        log_file=open(path+"UtilitiesLog.txt","a")
        log_file.write(str(time.time())+" error in count_files(): "+e.__str__()+"\n")
        log_file.close()

def find_tty_usb(idVendor, idProduct):
    """find_tty_usb('067b', '2302') -> '/dev/ttyUSB0'"""
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the enitre lot at once instead of going over all the usb devices
    # each time.
    for dnbase in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', dnbase)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        if idv != idVendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        if idp != idProduct:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(dnbase+':'):
                for subsubdir in os.listdir(join(dn, subdir)):
                    if subsubdir.startswith('ttyUSB'):
                        return join('/dev', subsubdir)       



        
        
