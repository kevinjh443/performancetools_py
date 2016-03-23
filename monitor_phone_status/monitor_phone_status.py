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
def root_device():
    print "-----------------------------------"
    Action(3)
    print "set your device screen on always; no lockscreen; user version; now will auto root:"
    x = raw_input("(y/n)?:")
    if 'y' in x:
        os.system("adb -s " + device_id + " shell am start -n com.jrdcom.user2root/.JrdUser2Root ")
        sleep(1)
        os.system("adb -s " + device_id + " shell input tap 180 340 ")
        print "please click the root button!"
        raw_input("Enter any key to continue:")
        print "wait root!"
        sleep(1)
        
        os.system("adb -s " + device_id + " shell input keyevent 3 ")
        os.system("adb -s " + device_id + " shell setprop ro.secure 0 ")
        os.system("adb -s " + device_id + " shell setprop ro.debuggable 1 ")
        os.system("adb -s " + device_id + " shell setprop ro.allow.mock.location 1 ")
        os.system("adb -s " + device_id + " shell setprop persist.sys.usb.config mtp,adb ")
        print "if error: device not found, please plug USB again now."
        os.system("adb wait-for-device ")
        sleep(1.5)
        os.system("adb -s " + device_id + " shell /system/bin/setenforce 0 ")
        os.system("adb root ")
        os.system("adb remount ")
        os.system("adb -s " + device_id + " shell setenforce 0 ")
        os.system("adb -s " + device_id + " shell input keyevent 3 ")

        print "root done!"
        sleep(1)
    else:
        print "no need root, please confirm you root first!"
        os.system("adb -s " + device_id + " shell setenforce 0 ")
        os.system("adb -s " + device_id + " shell input keyevent 3 ")
        sleep(2)


def check_phone_status(result_file_name, actionid):
    print "-----------------------------------"
    Action(actionid)
    os.system("adb -s "+ device_id +" shell date > "+result_file_name)
    
    os.system("adb -s "+ device_id +" shell getprop ro.build.type >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell getprop ro.tct.sys.ver : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell getprop ro.tct.sys.ver >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/adj : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/adj >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/minfree : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/minfree >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/vmpressure_file_min : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/vmpressure_file_min >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /proc/sys/vm/swappiness : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /proc/sys/vm/swappiness >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /proc/swaps : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /proc/swaps >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/enable_adaptive_lmk : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /sys/module/lowmemorykiller/parameters/enable_adaptive_lmk >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /proc/sys/vm/extra_free_kbytes : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /proc/sys/vm/extra_free_kbytes >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /sys/module/process_reclaim/parameters/enable_process_reclaim : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /sys/module/process_reclaim/parameters/enable_process_reclaim >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /proc/sys/vm/min_free_kbytes : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /proc/sys/vm/min_free_kbytes >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /proc/sys/vm/user_reserve_kbytes : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /proc/sys/vm/user_reserve_kbytes >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell dumpsys battery : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell dumpsys battery >> "+result_file_name)
    
    os.system("echo adb -s "+ device_id +" shell cat /proc/zoneinfo : >> "+result_file_name)
    os.system("adb -s "+ device_id +" shell cat /proc/zoneinfo >> "+result_file_name)
    
    sleep(1)
    print "Please check the parameters with parameter set file"
    if isWindowsSystem():
        os.system("notepad "+result_file_name)
    else:
        os.system("gedit "+result_file_name+" &")
    
    x = raw_input("(y/n)?:")
    if 'y' in x:
        print "checked OK!"
    else:
        print "n return"
        sys.exit(0)

def monitor_phone_status():
    Action(5)
    print "Please run the stress_test.py NOW!  and then please back to here run this script continue!!!"
    x = raw_input("(y/n)?:")
    if 'y' in x:
        print "monitor begain"
        create_monitor_file()
        os.system("echo 1 > stress_test_monitor_flag")
        record_date_monitor_file()
        flag=1
        while (flag == 1):
            try:
                record_monitor_data_to_file()
                
                f = open("stress_test_monitor_flag",'r')
                flag = int(f.readline().strip())
                f.close()
            except:
                print "have a issue return"
                break
            finally:
                print ""
        
        record_date_monitor_file()
        print "monitor end"
        
    else:
        print "n return"
        sys.exit(0)
        

def record_monitor_data_to_file():
    os.system("adb -s "+ device_id +" shell top -n 2 -d 2 -m 10 -t >> monito_phone_status-top.txt")
    os.system("adb -s "+ device_id +" shell vmstat >> monito_phone_status-vmstat.txt")
    os.system("adb -s "+ device_id +" shell dumpsys cpuinfo >> monito_phone_status-cpuinfo.txt")
    os.system("adb -s "+ device_id +" shell dumpsys meminfo >> monito_phone_status-meminfo.txt")
    print "monitor phone status ing....."
    print time.strftime('%Y-%m-%d %H:%M:%S')
    sleep(monitor_time_interval)
    

def record_date_monitor_file():
    os.system("adb -s "+ device_id +" shell date >> monito_phone_status-top.txt")
    os.system("adb -s "+ device_id +" shell date >> monito_phone_status-vmstat.txt")
    os.system("adb -s "+ device_id +" shell date >> monito_phone_status-cpuinfo.txt")
    os.system("adb -s "+ device_id +" shell date >> monito_phone_status-meminfo.txt")

def create_monitor_file():
    os.system("echo top > monito_phone_status-top.txt")
    os.system("echo vmstat > monito_phone_status-vmstat.txt")
    os.system("echo cpuinfo > monito_phone_status-cpuinfo.txt")
    os.system("echo meminfo > monito_phone_status-meminfo.txt")


#####################3, real do things##################

####################usage############################
def Usage():
    print 'monito_phone_status.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-a, --action: show the py do all the action'
    print '-t, --time interval:(default: 5) the monitor time interval'
    print '-------any thing can contacts author jianhua.he@tcl.com - Ext.66051'

def Version():
    print 'monito_phone_status.py 1.0.0.0.1'
    
def Action(action_id):
    if 1==action_id or action_id==action_print_all:
        print "Action 1 : choice device list"
    if 2==action_id or action_id==action_print_all:
        print "Action 2 : wait tester root device"
    if 3==action_id or action_id==action_print_all:
        print "Action 3 : root use this python script"
    if 4==action_id or action_id==action_print_all:
        print "Action 4 : check phone status"
    if 5==action_id or action_id==action_print_all:
        print "Action 5 : monitor phone status"
    if 6==action_id or action_id==action_print_all:
        print "Action 6 : check phone status again"
    
    
####################usage############################
####################4, monitor phone status###########################

####################4, monitor phone status###########################

if __name__ == "__main__":
    action_print_all=100
    monitor_time_interval=5
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvat', ['--action=','--interval='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif opt in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif opt in ('-a', '--action'):
            Action(action_print_all)
            sys.exit(0)
        elif opt in ('-t', '--interval'):
            try:
                monitor_time_interval=int(arg.strip())
            except:
                monitor_time_interval = 5
            finally:
                if monitor_time_interval < 2 or monitor_time_interval > 10:
                    monitor_time_interval=5
            print monitor_time_interval
        else:
            print 'unhandled option'
            sys.exit(3)
    
    Action(action_print_all)
    
    print "-----------------------------------"
    Action(1)
    device_id = select_device()
    
    print "-----------------------------------"
    Action(2)
    print "Please root your device. (*#*#212018#*#*); AND open the Logcat/Kernel logs"
    x = raw_input("(y/n)?:")
    if 'y' in x:
        print "continue"
    else:
        print "n return"
        sys.exit(0)
    
    root_device()
    check_phone_status("check_phone_status-begain.txt", 4)
    monitor_phone_status()
    check_phone_status("check_phone_status-end.txt", 6)
    
    
    print "All the stress test DONE! Please pull all the log to the test work path!"
    x = raw_input("(y/n)?:")
    print "DONE!!!"
    