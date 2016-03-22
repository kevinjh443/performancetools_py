#!/usr/bin/python
#coding=utf-8
#author: jianhua.he@tcl.com 2016-03-18

import re
import sys
import os
import platform
from subprocess import Popen, PIPE, call
from time import sleep
import getopt


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

    
    htmlfile.write("</table>")
    

#####################3, real do things##################

####################usage############################
def Usage():
    print 'stress_tesst.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-i, --input: (default:logcat_log.txt) input an input logcat txt file'
    print '-o, --output: (default:ANR_count_report.html) one html file report the ANR count detail information'
    print '-------any thing can contacts author jianhua.he@tcl.com - Ext.66051'

def Version():
    print 'ANR_count.py 1.0.0.0.1'
    
####################usage############################
####################4, monitor phone status###########################

####################4, monitor phone status###########################

if __name__ == "__main__":

    logcat_log_file="logcat_log.txt"
    reportFilename="ANR_count_report.html"
    
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
            logcat_log_file=arg
            print logcat_log_file
        elif opt in ('-o', '--output'):
            reportFilename=arg
            print reportFilename
        else:
            print 'unhandled option'
            sys.exit(3)
    
    htmlfile = open(reportFilename,'w')
    initHtml(htmlfile)
    
    file = open(logcat_log_file, "r")
    pattern = re.compile(r': ANR in (.*?)$')
    pattern_reason = re.compile(r'ActivityManager: Reason: (.*?)$')
    anr_count=0
    try:
        while True:
            line = file.readline()
            if line:
                match = re.search(pattern, line)
                match_reason = re.search(pattern_reason, line)
                if match:
                    anr_count += 1
                    print str(anr_count)+" ANR:"
                    print match.group(1).strip()
                    htmlfile.write(str(anr_count)+" ANR: </br>"+line+"</br>")
                elif match_reason:
                    print match_reason.group(1).strip()
                    htmlfile.write(match_reason.group(1).strip()+"</br></br>")
            else:
                break
    finally:
        file.close()
    
    
