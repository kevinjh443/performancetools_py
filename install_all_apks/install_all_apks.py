#!/usr/bin/python
#coding=utf-8
#author: jianhua.he@tcl.com 2016-03-18

import re
import sys
import os
import platform
import time
from subprocess import Popen, PIPE, call
from time import sleep
import getopt

#######################1, choice device#################
def select_device():
    device_list = get_device_list()
    if device_list:
        device_num = 0
        for device in device_list:
            print "%d -- %s" % (device_num, device)
            device_num += 1
    else:
        print "Cannot find devices!!!"
        sys.exit(1)
    print ""
    device_index = input("Please select one device: ")
    return device_list[device_index]

def get_device_list():
    dev_list = []
    call('adb start-server', shell=True)
    return_value = Popen('adb devices', shell=True, stdout=PIPE).stdout.readlines()
    for line in return_value:
        m_dev_id = re.match(r'(\w+)(?=\t)', line)
        if m_dev_id:
            dev_id = m_dev_id.group()
            dev_list.append(dev_id)
    return dev_list

def isWindowsSystem():
    return 'Windows' in platform.system()
#######################1, choice device#################

#######################2, html report method################

#######################2, html report method################

#####################3, real do things##################

#####################3, real do things##################

####################usage############################
    
####################usage############################


if __name__ == "__main__":
    
    device_id = select_device()
    install_all_apks_failure_report=device_id+"_install_all_apks_failure.txt"
    
    return_value=[]
    if isWindowsSystem():
        return_value = os.popen("dir /b *.apk").readlines()
    else:
        return_value = os.popen("ls ./*.apk").readlines()
    
    os.system("echo "+device_id+" > "+install_all_apks_failure_report)
    fuilure_count=0
    install_count=0
    for apkname in return_value:
        install_count += 1
        print str(install_count)+" : "+apkname
        cmd_line="adb -s "+ device_id +" install -r "+apkname
        print cmd_line
        return_value_suc = os.popen(cmd_line).readlines()
        for line in return_value_suc:
            if "Failure" in line:
                fuilure_count += 1
                print "Failure :"+apkname
                os.system("echo "+apkname+" : "+line+" >> "+install_all_apks_failure_report)
    print "Total Failure count = "+str(fuilure_count)+", neet to uninstall first!!!"
    if isWindowsSystem():
        os.system("notepad "+install_all_apks_failure_report)
    else:
        os.system("gedit "+install_all_apks_failure_report)
    print "DONE!!!"
    