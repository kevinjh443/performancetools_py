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
    
def write_report_table_title():
    initCode =""" 
    <table class="table" border=1 cellspacing='0' cellpadding='0'>
    <tr> 
    <th class="spec">time</th> 
    <th>user</th> 
    <th>system</th> 
    <th>iow</th> 
    <th>iow num</th> 
    <th>irq</th> 
    </tr> 
    """
    htmlfile.write(initCode)
    
def write_report_table_end():
    initCode =""" 
    </table>
    """
    htmlfile.write(initCode)
#######################2, html report method################

#####################3, real do things##################
def check_phone_status():
    print "check phone status"

def check_iow():
    print "check iow"
    file = open(folder_file+"/monito_phone_status-top.txt", "r")
    pattern = re.compile(r'User (.*?)%, System (.*?)%, IOW (.*?)%, IRQ (.*?)%')
    try:
        write_report_table_title()
        distri=[0,0,0,0,0,0,0,0,0,0,0]
        while True:
            line = file.readline()
            if line:
                match = re.search(pattern, line)
                if match:
                    user =  match.group(1).strip()
                    system =  match.group(2).strip()
                    iow =  match.group(3).strip()
                    irq =  match.group(4).strip()
                    htmlfile.write("<tr> <td> </td> <td> "+user+"</td> <td> "+system+"</td> <td> "+iow+"</td> <td> </td> <td> "+irq+"</td> </tr>")
                    print "<tr> <td> </td> <td> "+user+"</td> <td> "+system+"</td> <td> "+iow+"</td> <td> </td> <td> "+irq+"</td> </tr>"
                    iow_num = int(iow)
                    if iow_num == 0 or iow_num >= 100:
                        temp = distri[0]
                        temp += 1
                        distri[0] = temp
                    elif iow_num < 10:
                        temp = distri[1]
                        temp += 1
                        distri[1] = temp
                    elif iow_num >= 10 and iow_num < 20:
                        temp = distri[2]
                        temp += 1
                        distri[2] = temp
                    elif iow_num >= 20 and iow_num < 30:
                        temp = distri[3]
                        temp += 1
                        distri[3] = temp
                    elif iow_num >= 30 and iow_num < 40:
                        temp = distri[4]
                        temp += 1
                        distri[4] = temp
                    elif iow_num >= 40 and iow_num < 50:
                        temp = distri[5]
                        temp += 1
                        distri[5] = temp
                    elif iow_num >= 50 and iow_num < 60:
                        temp = distri[6]
                        temp += 1
                        distri[6] = temp
                    elif iow_num >= 60 and iow_num < 70:
                        temp = distri[7]
                        temp += 1
                        distri[7] = temp
                    elif iow_num >= 70 and iow_num < 80:
                        temp = distri[8]
                        temp += 1
                        distri[8] = temp
                    elif iow_num >= 80 and iow_num < 90:
                        temp = distri[9]
                        temp += 1
                        distri[9] = temp
                    elif iow_num >= 90 and iow_num < 100:
                        temp = distri[10]
                        temp += 1
                        distri[10] = temp
            else:
                break
    finally:
        write_report_table_end()
        htmlfile.write("<table><tr> <td> 0 or > 100 </td> <td> 1<=x<10 </td> <td> 10<=x<20 </td><td> 20<=x<30 </td><td> 30<=x<40 </td><td> 40<=x<50 </td><td> 50<=x<60 </td><td> 60<=x<70 </td><td> 70<=x<80 </td><td> 80<=x<90 </td><td> 90<=x<100 </td></tr>")
        htmlfile.write("<tr>")
        for temp in distri:
            htmlfile.write("<td> "+str(temp)+" </td>")
        htmlfile.write("</tr></table>")
        file.close()

#####################3, real do things##################

####################usage############################
def Usage():
    print 'stress_tesst.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-i, --input: (default:idol4) input an folder of stress performance test result'
    print '-o, --output: (default:stress_performance_report.html) one html file report the stress test detail statistics information'
    print '-------any thing can contacts author jianhua.he@tcl.com - Ext.66051'

def Version():
    print 'stress_tesst.py 1.0.0.0.1'
    
####################usage############################
####################4, monitor phone status###########################

####################4, monitor phone status###########################

if __name__ == "__main__":
    folder_file="idol4"
    reportFilename="stress_performance_report.html"
    
    print "---------device list----------"
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvi:o:', ['input=','output='])
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
            folder_file = arg
            print folder_file
        elif opt in ('-o', '--output'):
            reportFilename=arg
            print reportFilename
        else:
            print 'unhandled option'
            sys.exit(3)
    
    htmlfile = open(folder_file+"/"+reportFilename,'w')
    initHtml(htmlfile)
    
    ############1, check the phone status################
    check_phone_status()
    
    check_iow()
    
    htmlfile.write("</body> </html>")
    htmlfile.close()
    
        
        