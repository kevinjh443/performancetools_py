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
import threading

###########global########################
global stress_degree_update_factor
global running_times

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
def initHtml(htmlfile):
    '''write basic html file'''
    initCode = """<html><head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title>app start report</title>
    <style type="text/css"> 
    .table 
    { 
    width: 80%; 
    padding: 0; 
    margin: 0; 
    } 
    th { 
    font: bold 12px "Trebuchet MS", Verdana, Arial, Helvetica, sans-serif; 
    color: #4f6b72; 
    border-right: 1px solid #C1DAD7; 
    border-bottom: 1px solid #C1DAD7; 
    border-top: 1px solid #C1DAD7; 
    letter-spacing: 2px; 
    text-transform: uppercase; 
    text-align: left; 
    padding: 6px 6px 6px 12px; 
    background: #CAE8EA no-repeat; 
    } 
    .tdimpotant {
    background: #77DDFF;
    font-weight:bold;
    }
    td { 
    border-right: 1px solid #C1DAD7; 
    border-bottom: 1px solid #C1DAD7; 
    background: #fff; 
    font-size:14px; 
    padding: 6px 6px 6px 12px; 
    color: #4f6b72; 
    } 
    td.alt { 
    background: #F5FAFA; 
    color: #797268; 
    } 
    th.spec,td.spec { 
    border-left: 1px solid #C1DAD7; 
    } 
    /*---------for IE 5.x bug*/ 
    html>body td{ font-size:14px;} 
    tr.select th,tr.select td 
    { 
    background-color:#CAE8EA; 
    color: #797268; 
    } 
    </style>
    <head><body>
    <center>
    </br>

    """
    htmlfile.write(initCode)
#######################2, html report method################

#####################3, real do things##################

def get_apps_info(app_info_file):
    global stress_degree_update_factor
    global running_times
    app_info_temp={}
    
    pattern = re.compile(r': (.*?) : (\d.*?)')
    file = open(os.path.dirname(os.path.abspath(__file__)) + os.sep+ app_info_file, "r")
    lists = file.readlines()
    file.close()
    for line in lists:
        match = re.search(pattern, line)
        if match:
            app_name = match.group(1).strip()
            app_type = match.group(2).strip()
            
            if app_type == "3":
                running_times += high_type_run_count
            elif app_type == "2":
                running_times += mid_type_run_count
            elif app_type == "1":
                running_times += low_type_run_count
            
            print app_type+" : "+app_name
            app_type = list(app_type)
            app_type.append(0)#start count
            app_type.append(0)#monkey count
            app_info_temp[app_name] = app_type
    
    return app_info_temp

def homekey_exit_app():
    print "exit home key"
    cmd_line1 = "adb -s " + device_id + " shell input keyevent 3"#home key
    os.popen(cmd_line1)
    sleep(1)

def double_homekey_exit_app():
    print "double - exit home key"
    cmd_line1 = "adb -s " + device_id + " shell input keyevent 3"#home key
    os.popen(cmd_line1)
    sleep(0.05)
    os.popen(cmd_line1)
    sleep(1)

def get_package_name(app):
    appinfo = app.split("/")
    pakname = appinfo[0].strip()
    return pakname


class ThreadStartApp(threading.Thread):
    def __init__(self, app, device_id):
        threading.Thread.__init__(self)
        self.app = app
        self.device_id = device_id
    
    def run(self):
        cmd_line = "adb -s " + self.device_id + " shell am start -W -n " + self.app
        print cmd_line
        htmlfile.write(cmd_line+" </br>")
        result = os.popen(cmd_line).readlines()
        for line in result:
            print line
        sleep(1)
        homekey_exit_app()
        
class ThreadRunningMonkey(threading.Thread):
    def __init__(self, packagename, device_id, type_monkey_count, need_update_stress_degree):
        threading.Thread.__init__(self)
        self.packagename = packagename
        self.device_id = device_id
        self.type_monkey_count = type_monkey_count
        self.need_update_stress_degree = need_update_stress_degree
          
    def run(self):
        throttle = 100
        if self.need_update_stress_degree:
            throttle = 200
        
        cmd_line = "adb -s " + self.device_id + " shell monkey -p "+ self.packagename +" --throttle "+str(throttle)+" -s 10 -v --ignore-crashes --ignore-timeouts --ignore-security-exceptions "+str(self.type_monkey_count)
        print cmd_line
        htmlfile.write(cmd_line+" </br>")
        result = os.popen(cmd_line).readlines()
        sleep(1)
        print " monke done!"
        double_homekey_exit_app()

def check_if_need_stress_degree_update():#have rest long time, the lower stress
    global stress_degree_update_factor
    global running_times
    
    need_stress_degree_update = False
    stress_degree_update_factor += 1
    print "*****speed****"+str(stress_degree_update_factor)+"/"+str(running_times)+"*******"
    if app_num >= 20 and running_times >= 30:
        up_limit = running_times * 0.7
        down_limit = running_times * 0.5# 0.7-0.5 = 20% need stress update
        print "down = "+str(down_limit)+"; up = "+str(up_limit)
        if stress_degree_update_factor <= up_limit and stress_degree_update_factor >= down_limit:
            need_stress_degree_update = True
    print "this time if need update stress degree : "+str(need_stress_degree_update)
    return need_stress_degree_update

def check_adb_status():
    check_adb_wait_time = time.time()
    print "check adb status: if waiting here long time, adb have issue, please plug USB again now."
    os.system("adb wait-for-device ")
    check_adb_wait_time = time.time() - check_adb_wait_time
    if check_adb_wait_time >= 5:
        htmlfile.write("wait adb long time : [wait-for-device "+str(check_adb_wait_time)+"] </br>")
        print "record : wait adb long time : [wait-for-device "+str(check_adb_wait_time)+"]"
    else:
        print "adb status is OK"
    

def type_diff_run(app, app_info, type_run_count, type_monkey_count, is_last_loop):
    app_type = app_info.get(app);
    app_type = list(app_type)
    
    print "is last loop:"+str(is_last_loop)
    if is_last_loop:
        run_count_now = type_run_count - app_type[1]
    else:
        run_count_now = int(round(float(float(type_run_count) / complete_loop_time), 0))
    
    ###################check adb status###############
    check_adb_status()
    
    ###################launch app#####################
    for i in range(run_count_now-1):
        
        if check_if_need_stress_degree_update():
            sleep(3);
        
        thread_start = ThreadStartApp(app, device_id)
        start_time = time.time()
        thread_start.start()
        thread_start.join(7)
        now_time = time.time()
        
        now_time = now_time - start_time
        now_time = now_time - 2
        
        if now_time < 0:
            now_time = 0
        elif now_time >= 5 :
            print "time out here! = ["+str(now_time)+" sec]"
            
        htmlfile.write("["+str(now_time)+" sec]"+" </br>")
        print "["+str(now_time)+" sec]"+" </br>"
        
        if thread_start.is_alive():
            print "thread_start still alive, need wait exit!"
            double_homekey_exit_app()
    
    
    ####################moneky test##################
    need_update_stress_degree = check_if_need_stress_degree_update()
    if need_update_stress_degree:
        sleep(2)
    
    thread_monkey = ThreadRunningMonkey(get_package_name(app), device_id, type_monkey_count, need_update_stress_degree)
    monkey_start_time = time.time()
    thread_monkey.start()
    temp_timeout = int(round(float(float(type_monkey_count) / 100), 0))
    temp_timeout = temp_timeout * 6
    if need_update_stress_degree:
        temp_timeout = temp_timeout * 2
    print "\n set monkey timeout : "+str(temp_timeout)
    thread_monkey.join(temp_timeout)
    monkey_now_time = time.time()
    
    monkey_now_time = monkey_now_time - monkey_start_time
    monkey_time = monkey_now_time - 2.05
    
    if monkey_now_time >= temp_timeout:
        print "monkey time out here! = [monkey "+str(monkey_now_time)+" sec]"
    elif monkey_time < 0:
        monkey_time = 0
    
    htmlfile.write("[monkey "+str(monkey_time)+" sec]"+" </br>")
    print "[monkey "+str(monkey_time)+" sec]"+" </br>"
    
    if thread_monkey.is_alive():
        print "thread_monkey still alive, need wait exit!"
        double_homekey_exit_app()
    
    #############update the test times###############
    app_type[1] = run_count_now + app_type[1]
    app_type[2] = type_monkey_count + app_type[2]
    app_info[app] = app_type


def test_stress(app_info, is_last_loop):
    for app in app_info:
        
        app_type = app_info.get(app);
        app_type = list(app_type)
        if "3" == app_type[0]:
            print "type 3 high: running"
            type_diff_run(app, app_info, high_type_run_count, high_type_monkey_count, is_last_loop)
        elif "2" == app_type[0]:
            print "type 2 mid: running"
            type_diff_run(app, app_info, mid_type_run_count, mid_type_monkey_count, is_last_loop)
        else:
            print "type 1 low: running"
            type_diff_run(app, app_info, low_type_run_count, low_type_monkey_count, is_last_loop)
        

def write_report(app_info):
    initCode =""" 
    <table class="table" border=1 cellspacing='0' cellpadding='0'>
    <tr> 
    <th class="spec">apk name</th> 
    <th>user type</th> 
    <th>launch count</th> 
    <th>monkey count</th> 
    </tr> 
    """
    htmlfile.write(initCode)
    
    for app in app_info:
        info = "<tr><td>"+get_package_name(app)+"</td>"
        app_type = app_info.get(app);
        app_type = list(app_type)
        if "3" == app_type[0]:
            info += "<td> High </td>"
        elif "2" == app_type[0]:
            info += "<td> Mid </td>"
        else:
            info += "<td> low </td>"
        info += "<td> "+str(app_type[1])+" </td>"
        info += "<td> "+str(app_type[2])+" </td> </tr>"
        htmlfile.write(info)
    
    htmlfile.write("</table>")
    

#####################3, real do things##################

####################usage############################
def Usage():
    print 'stress_tesst.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-i, --input: (default:stress_app_info.txt) input an input txt file, the app information from file; if -i /sdcard/Apps.txt will auto pull from device'
    print '-o, --output: (default:stress_performance_auto_test_report.html) one html file report the stress test detail information'
    print '--high: like --high="9 2000" (default:9 2000) mean high type app will launch 9 times and the monkey will run 2000 times '
    print '--mid: like --mid="9 2000" (default:6 1000) mean mid type app will launch 9 times and the monkey will run 2000 times '
    print '--low: like --low="9 2000" (default:3 500) mean low type app will launch 9 times and the monkey will run 2000 times '
    print '--loop: like --loop=3 (default:3) mean all the high mid low app will loop 3 times complete all the test '
    print '-------any thing can contacts author jianhua.he@tcl.com - Ext.66051'

def Version():
    print 'stress_tesst.py 1.0.0.0.1'
    
####################usage############################
####################4, monitor phone status###########################

####################4, monitor phone status###########################

if __name__ == "__main__":
    high_type_run_count = 9
    high_type_monkey_count = 1000
    mid_type_run_count = 6
    mid_type_monkey_count = 600
    low_type_run_count = 3
    low_type_monkey_count = 400
    complete_loop_time=3
    
    global stress_degree_update_factor
    global running_times
    stress_degree_update_factor = 0
    running_times = 0
    app_info_file="stress_app_info.txt"
    reportFilename="stress_performance_auto_test_report.html"
    
    print "---------device list----------"
    device_id = select_device()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvi:o:', ['input=','output=', 'high=', 'mid=', 'low=', 'loop='])
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
        elif opt in ('-i', '--input'):
            if "/sdcard/Apps.txt" == arg:
                result = os.popen("adb -s " + device_id + " pull /sdcard/Apps.txt .").readlines()
                app_info_file="Apps.txt"
            else:
                app_info_file=arg
            print app_info_file
        elif opt in ('-o', '--output'):
            reportFilename=arg
            print reportFilename
        elif opt in ('--high',):
            print arg
            try:
                arg = arg.split(" ")
                high_type_run_count = int(arg[0].strip())
                high_type_monkey_count = int(arg[1].strip())
            except:
                high_type_run_count = high_type_run_count
                high_type_monkey_count = high_type_monkey_count
            print high_type_run_count
            print high_type_monkey_count
        elif opt in ('--mid',):
            print arg
            try:
                arg = arg.split(" ")
                mid_type_run_count = int(arg[0].strip())
                mid_type_monkey_count = int(arg[1].strip())
            except:
                mid_type_run_count = mid_type_run_count
                mid_type_monkey_count = mid_type_monkey_count
            print mid_type_run_count
            print mid_type_monkey_count
        elif opt in ('--low',):
            print arg
            try:
                arg = arg.split(" ")
                low_type_run_count = int(arg[0].strip())
                low_type_monkey_count = int(arg[1].strip())
            except:
                low_type_run_count = low_type_run_count
                low_type_monkey_count = low_type_monkey_count
            print low_type_run_count
            print low_type_monkey_count
        elif opt in ('--loop',):
            complete_loop_time=int(arg)
            print complete_loop_time
        else:
            print 'unhandled option'
            sys.exit(3)
    
    htmlfile = open(reportFilename,'w')
    initHtml(htmlfile)
    
    ############read app info################
    app_info = get_apps_info(app_info_file)
    app_num = len(app_info)
    print "It expected to "+str(running_times / 3)+" minutes to complete....."
    x = input("Press 1 key to continue:")
    ###########run those app############
    test_start_time = time.time()
    for j in range(complete_loop_time):
        if j == (complete_loop_time-1):
            test_stress(app_info, True)
        else:
            test_stress(app_info, False)
    
    test_end_time = time.time()
    print "------------------------------"
    htmlfile.write(" </br></br></br> total run time = "+str(test_end_time-test_start_time)+" sec")
    print app_info
    write_report(app_info)
    htmlfile.write("</body> </html>")
    htmlfile.close()
    
    #flish the monitor phone STATUS
    os.system("echo 0 >stress_test_monitor_flag")
        
        