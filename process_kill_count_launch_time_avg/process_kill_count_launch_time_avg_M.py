#!/usr/bin/python

import time
import datetime
import re
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import glob
import email
from commands import *
import getopt

global record_be_time_flag
global begain_time
global end_time
global log_begain_time
global log_end_time
global have_log_time_flag

def record_be_time(line):
	match = re.search(pattern_time, line)
	if match:
# 		month = int(match.group(1).strip())
# 		day = int(match.group(2).strip())
# 		hour = int(match.group(3).strip())
# 		minute = int(match.group(4).strip())
# 		second = int(match.group(5).strip())
# 		min_sec = int(match.group(6).strip())
		l_time = match.group().strip()
		l_time = l_time[:-4]
		print l_time
		log_time = time.mktime(time.strptime(l_time,'%m-%d %H:%M:%S'))
		#print log_time
		global record_be_time_flag
		global begain_time
		global end_time
		if record_be_time_flag == 0:
			record_be_time_flag += 1
			begain_time=log_time
			end_time=log_time
 			
		if (float(log_time) < float(begain_time)):
			begain_time=log_time
		elif (float(log_time) > float(end_time)):
			end_time=log_time
			
def record_be_time_have_log_time(line):
	global log_begain_time
	global log_end_time
	match = re.search(pattern_time, line)
	if match:
		l_time = match.group().strip()
		l_time = l_time[:-4]
		print l_time
		log_time = time.mktime(time.strptime(l_time,'%m-%d %H:%M:%S'))
		#print log_time
		global record_be_time_flag
		global begain_time
		global end_time
 		
 		if float(log_time) < float(log_begain_time):
 			return False
 		elif float(log_time) > float(log_end_time):
 			return False
 		else:
 			if record_be_time_flag == 0:
				record_be_time_flag += 1
				begain_time=log_time
				end_time=log_time
			if (float(log_time) < float(begain_time)):
				begain_time=log_time
			elif (float(log_time) > float(end_time)):
				end_time=log_time
			return True

####################usage############################
def Usage():
    print 'process_kill_count_launch_time_avg_M.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '--begain,the begain test time like : --begain="01-01 02:32:32".'
    print '--end,the end test time like : --end="01-01 02:32:32".'
    print '-------any thing can contacts author jianhua.he@tcl.com - Ext.66051'

def Version():
    print 'stress_tesst.py 1.0.0.0.1'
    
####################usage############################

if __name__ == "__main__":
	global log_begain_time
	global log_end_time
	global have_log_time_flag
	have_log_time_flag=0
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hvi:o:', ['input=','output=','begain=','end='])
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
		elif opt in ('--begain'):
			log_begain_time = time.mktime(time.strptime(arg,'%m-%d %H:%M:%S'))
			print arg+" = "+str(log_begain_time)
			have_log_time_flag += 1
		elif opt in ('--end'):
			log_end_time = time.mktime(time.strptime(arg,'%m-%d %H:%M:%S'))
			print arg+" = "+str(log_end_time)
			have_log_time_flag += 1
		else:
			print 'unhandled option'
			sys.exit(3)
			
	global record_be_time_flag
	global begain_time
	global end_time
	record_be_time_flag=0
	begain_time=0
	end_time=0
	pattern_time = re.compile(r'(\d+.*?)-(\d+.*?) (\d+.*?):(\d+.*?):(\d+.*?).(\d\d\d.*?) ')
	
	
	
	os.system("mv *.txt log-f")
	os.system("gzip -d *.gz")
	
	results = getoutput("ls *.txt")
	lines = results.split('\n')
	for line in lines:
		os.system("cat %s >> log-f"%line)
		print line
		print "------"
	os.system("mv log-f log-f.txt")
	
	
	sum_kill_count = 0
	sum_avg = 0
	sum_avg_count = 0
	avg_p = 0
	
	
	
	
	file_name = "log-f.txt"
	
	kill_relaunch_names = []
	all_names = []
	time_names = []
	service_names = []
	kill_activity = []
	
	
				
	
	if os.path.isfile(file_name):
		tmp_file = open(file_name,"r")
		tmp_lines = tmp_file.readlines()
		i = 0
		print "++++++++++++++++++++++++++++++ start to get Killed Re-launch+++++++++++++++++++++++++++++++++++++++++++++++++"
		if tmp_lines:
			for line in tmp_lines:
				if ("Start proc" in line) and ("ActivityManager" in line):
					if have_log_time_flag != 2:
						record_be_time(line)
						print line
						name1=line.split(":")[4]
						name2=name1.split("/")[0]
						name3=line.split("/")[1]
		                                name4=name3.split(" ")[-1]
						if name2 == name4:
							print name2
							if name2 == "system":
								print "kill"
							kill_relaunch_names.append(name4)
							if "for activity" in line:
								if name2 == "system":
									print "activity"
								kill_activity.append(name4)
					elif have_log_time_flag == 2 and record_be_time_have_log_time(line):
						print "have log time:"+line
						name1=line.split(":")[4]
						name2=name1.split("/")[0]
						name3=line.split("/")[1]
		                                name4=name3.split(" ")[-1]
						if name2 == name4:
							print name2
							if name2 == "system":
								print "kill"
							kill_relaunch_names.append(name4)
							if "for activity" in line:
								if name2 == "system":
									print "activity"
								kill_activity.append(name4)
	
		print "++++++++++++++++++++ start to get all start count+++++++++++++++++++++++++++++++"
		if tmp_lines:
			for line in tmp_lines:
				if ("ActivityManager" in line) and ("START u0" in line):
					if have_log_time_flag != 2:
						record_be_time(line)
						print line
						name1=line.split("/")[-2].strip()
						name2=name1.split("=")[-1].strip()
						print name2
						if name2 == "system":
							print "cache"
						all_names.append(name2)
					elif have_log_time_flag == 2 and record_be_time_have_log_time(line):
						print "have log time:"+line
						name1=line.split("/")[-2].strip()
						name2=name1.split("=")[-1].strip()
						print name2
						if name2 == "system":
							print "cache"
						all_names.append(name2)
	
		print "++++++++++++++++++++++++++++++++++ start to get service kill count +++++++++++++++++++++++++++++++++++++++++++++++++++++"
		if tmp_lines:
			for line in tmp_lines:
				if ("ActivityManager" in line) and ("Killing" in line):
					if have_log_time_flag != 2:
						record_be_time(line)
						print line
						line1=re.match('(\d\d-\d\d\s+\d\d:\d\d:\d\d\.\d+\s+\d+\s+\+\d+s+\w\s)ActivityManager: Killing\s\d+\w+',line)
						if line1:
							name1=line1.split("/")[-2].strip().split(":")[-1]
							print name1
							service_names.append(name1)
					elif have_log_time_flag == 2 and record_be_time_have_log_time(line):
						print "have log time:"+line
						line1=re.match('(\d\d-\d\d\s+\d\d:\d\d:\d\d\.\d+\s+\d+\s+\+\d+s+\w\s)ActivityManager: Killing\s\d+\w+',line)
						if line1:
							name1=line1.split("/")[-2].strip().split(":")[-1]
							print name1
							service_names.append(name1)
	
	
		#sort kill_relaunch_names
		s_kill_relaunch_names = []
		for name in kill_relaunch_names:
			if name not in s_kill_relaunch_names:
				s_kill_relaunch_names.append(name)
	
		#sort kill_activity
		s_kill_activity = []
		for name in kill_activity:
			if name not in s_kill_activity:
				s_kill_activity.append(name)
	
		#sort all_names
		s_all_names = []
		for name in all_names:
			if name not in s_all_names:
				s_all_names.append(name)
	
		#sort my all names
		my_all = kill_relaunch_names + all_names
		tmp_all = []
		for m_all in my_all:
			if m_all not in tmp_all:
				tmp_all.append(m_all)
	
		print "+++++++++++++++ mail ++++++++++++++++++"
	   	htmlPart = MIMEBase('text', 'html', charset="us-ascii")
		html = '<html xmlns="http://www.w3.org/1999/xhtml">'
	    	html += '<head>'
		html += '<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />'
	    	html += '</head>'
	    	html += '<body>'
		html += '<br></font>'
		html += '<br><font color="#ff0000" face="Arial" size="2">Summary:<br></font>'
		html += '<style><!-- BODY,DIV,TABLE,THEAD,TBODY,TFOOT,TR,TH,TD,P { font-family:"Arial"; font-size:x-small } --></style>'
		html += '<table border="0" cellspacing="0" cols="12" rules="none">'
		html += '<tr>'
		html += '<td style="border: 1px solid rgb(0, 0, 0);" align="center" bgcolor="#ff9900" height="23" valign="middle"><b>'+'Name'+'</b></td>'
		html += '<td style="border: 1px solid rgb(0, 0, 0);" align="center" bgcolor="#ff9900" height="23" valign="middle"><b>'+'process kill count'+'</b></td>'
		html += '<td style="border: 1px solid rgb(0, 0, 0);" align="center" bgcolor="#ff9900" height="23" valign="middle"><b>'+'Display Activity AVG Time'+'</b></td>'
		html += '</tr>'
	
		#get name's count for very rules
		for t_all in tmp_all:
			if (t_all in kill_relaunch_names) or (t_all in all_names):
				print t_all
				print kill_relaunch_names.count(t_all)
				print all_names.count(t_all)
				print kill_activity.count(t_all)
				k_count = kill_relaunch_names.count(t_all)
				a_count = all_names.count(t_all)-kill_activity.count(t_all)
				print "---------------"
				html += '<tr>'
				html += '<td style="border: 1px solid rgb(0, 0, 0);" align="center" bgcolor="#ff9900" height="23" valign="middle"><b>'+t_all+'</b></td>'
				html += '<td style="border: 1px solid rgb(0, 0, 0);" align="center" bgcolor="#ff9900" height="23" valign="middle"><b>'+str(k_count)+'</b></td>'
				sum_kill_count = sum_kill_count + k_count
	
				print "++++++++++++++++++++++++++++++++++ start to get show time +++++++++++++++++++++++++++++++++++++++++++++++++++++"
				avg_time = 0
				avg_count = 0
				if tmp_lines:
					for line in tmp_lines:
						if ("ActivityManager" in line) and ("Displayed" in line) and ("+" in line) and (t_all in line):
							print line
							main_time=line.split(":")[-1].strip()
							if len(main_time) > 12:
								tmp_str = main_time.split(" ")[0].strip()
								time1 = tmp_str[1:].strip()
								if time1.count("m") == 2:
									mint = time1.split("m")[0]
									second = time1.split("s")[0].split("m")[1]
									ms = time1.split("m")[1].split("s")[1]
									avg_time = int(mint)*60*1000 + int(ms) + int(second)*1000 + avg_time
									avg_count = avg_count + 1
								elif time1.count("s") == 2:
									mint = 0
									second = time1.split("s")[0]
									ms = time1.split("s")[1][0:-1]
									avg_time = int(mint)*60*1000 + int(ms) + int(second)*1000 + avg_time
									avg_count = avg_count + 1
								elif (time1.count("s") == 1) and (time1.count("m") == 1):
									mint = 0
									second = 0
									ms = time1.split("m")[0]
									avg_time = int(mint)*60*1000 + int(ms) + int(second)*1000 + avg_time#kevin ho fix bug 
									avg_count = avg_count + 1
							elif main_time.count("m") == 2:
								time1 = main_time[1:].strip()
								mint = time1.split("m")[0]
								second = time1.split("s")[0].split("m")[1]
								ms = time1.split("m")[1].split("s")[1]
								avg_time = int(mint)*60*1000 + int(ms) + int(second)*1000 + avg_time
								avg_count = avg_count + 1
							elif main_time.count("s") == 2:
								time1 = main_time[1:].strip()
								mint = 0
								second = int(time1.split("s")[0])
								ms = time1.split("s")[1][0:-1]
								avg_time = int(mint)*60*1000 + int(ms) + int(second)*1000 + avg_time
								avg_count = avg_count + 1
							elif (main_time.count("s") == 1) and (main_time.count("m") == 1):
								avg_time = int(main_time[1:-2]) + avg_time
								avg_count = avg_count + 1
							else:
								print "++++++++++++++++++++++++"
								print "time is wrong!!!"
								sys.exit(1)
	
	
				if float(avg_count) == 0:
					my_time = 0
					print t_all
				else:
					
					tmp_time = (float(avg_time)/float(avg_count)/1000)
					my_time = "%.3f"%tmp_time
					sum_avg = sum_avg + float(my_time)
					if (str(my_time) != "0") and (str(my_time) != "0.000"):
						sum_avg_count = sum_avg_count + 1
					
				html += '<td style="border: 1px solid rgb(0, 0, 0);" align="center" bgcolor="#ff9900" height="23" valign="middle"><b>'+str(my_time)+'</b></td>'
				html += '</tr>'
			else:
				print t_all
				print "+++++++++++++ It can not find up model  ++++++++++++++++"
				sys.exit(1)
		tmp_file.close()
		if sum_avg_count == 0:
			avg_p = 0
		else:
			tmp_avg = sum_avg/float(sum_avg_count)
			avg_p = "%.3f"%tmp_avg
		print "++++++++++++++++++++++++++++++++++++++"
		print "Process Killed Count is : " + str(sum_kill_count) + "\n"
		print "Display Activity AVG Time(s) : " + str(avg_p) + "\n"
		print "++++++++++++++++++++++++++++++++++++++"
		html += '</table>'
		html += '</body>'
	    	html += '<p><font color="gray" size="4px">'
	        html += '&nbsp;&nbsp;&nbsp;&nbsp Process Killed Count is : %s <br />'%str(sum_kill_count)
	        html += '&nbsp;&nbsp;&nbsp;&nbsp Display Activity AVG Time(s) : %s <br />'%str(avg_p)
	    	html += '</font></p>'
	    	
	    	time_begain_temp=time.strftime('%m-%d %H:%M:%S',time.localtime(begain_time))
	    	time_end_temp=time.strftime('%m-%d %H:%M:%S',time.localtime(end_time))
	    	if have_log_time_flag == 2:
	    		print "+++++++++++++++++++TEST BEGAIN AT -GAP+++++++++++++++++++"
		    	print "the TEST Begain at : "+time.strftime('%m-%d %H:%M:%S',time.localtime(log_begain_time))
		    	print "the TEST End at : "+time.strftime('%m-%d %H:%M:%S',time.localtime(log_end_time))
		    	print "+++++++++++++++++++TEST END AT -GAP+++++++++++++++++++"
		    	html +=  "</br>+++++++++++++++++++TEST BEGAIN AT -GAP+++++++++++++++++++"
		    	html +=  "</br>the TEST Begain at : "+time.strftime('%m-%d %H:%M:%S',time.localtime(log_begain_time))
		    	html +=  "</br>the TEST End at : "+time.strftime('%m-%d %H:%M:%S',time.localtime(log_end_time))
		    	html +=  "</br>+++++++++++++++++++TEST END AT -GAP+++++++++++++++++++"
	    	print "+++++++++++++++++++First Item at -GAP+++++++++++++++++++"
	    	print "the first action item begain at : "+time_begain_temp
	    	print "the last action item end at : "+time_end_temp
	    	print "+++++++++++++++++++Last Item at -GAP+++++++++++++++++++"
	    	html += "</br>+++++++++++++++++++First Item at -GAP+++++++++++++++++++"
	    	html +=  "</br>the first action item begain at : "+time_begain_temp
	    	html +=  "</br>the last action item end at : "+time_end_temp
	    	html += "</br>+++++++++++++++++++Last Item at -GAP+++++++++++++++++++"

	    	html += '<p><font color="gray" size="2px">'
	    	html += 'Best Regards,<br />'
	    	html += 'ADDR: No.232, Tower C, Liangjing Rd, Zhangjiang High-Teck Park, Pudong Shanghai 201203. P. R. China'
	    	html += '</font></p>'
	    	htmlPart.set_payload(html)
	    	encoders.encode_base64(htmlPart)
		gettime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		fh = open("%s_result.html"%gettime,'w')
		fh.write(html)
		fh.close
		print "The result html path is %s_result.html"%gettime








