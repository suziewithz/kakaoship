# -*- coding: utf8 -*-

import sys
from datetime import datetime
from dateutil import parser

class Msg:
	def __init__(self):
		datetime = ""
		sender = ""
		contents = ""

log_file = open (sys.argv[1] , 'r')


info = log_file.readline()
logs = log_file.readlines()

messages = []

message_origin = ""

# mac no difference between locales.
if "Date,User,Message" in info :
	message_origin = "mac"

	for log in logs :
		try :
			msg = Msg() 
			msg.datetime = datetime.strptime(log.split(",")[0], '%Y-%m-%d %H:%M:%S')
			msg.sender = log.split(",")[1][1:-1]
			msg.contents = log.split(",")[2][1:-2]
			messages.append(msg)
		except :
			print log

# window
elif "with KakaoTalk Chats" in info :
	message_origin = "win"
	message_date = ""
	for log in logs:
		
		#window en
		try :
			temp_log = unicode(log,'utf-8')
			temp_log = temp_log.replace("-", "")
			message_date = datetime.strptime(temp_log, ' %A, %B %d, %Y ')
			print message_date
		except :
			pass
		# window kr
		try :
			temp_log = unicode(log,'utf-8')
			temp_log = temp_log.replace("-", "")
			temp_log = temp_log.replace("년".decode('utf-8'), "")
			temp_log = temp_log.replace("월".decode('utf-8'), "")
			temp_log = temp_log.replace("일".decode('utf-8'), "")
			temp_log = filter(lambda x: x.isdigit() or x.isspace(), temp_log)
			message_date = datetime.strptime(temp_log,' %Y %m %d  \n')
			print message_date
		except:
			pass

		#window en
		try :
			msg = Msg()
			msg.sender = log.split("]")[0][1:]
			message_time = datetime.strptime(log.split("]")[1][2:], "%H:%M %p")
			msg.datetime = datetime.combine(message_date ,message_time.timetz())
			msg.contents = log.split("]")[2][1:-1]
			messages.append(msg)
		except :
			pass

		#window kr
		try :
			msg = Msg()
			msg.sender = log.split("]")[0][1:]
			dt = unicode(log.split("]")[1][2:], 'utf-8')
			dt = dt.replace("오전".decode('utf-8'), "AM")
			dt = dt.replace("오후".decode('utf-8'), "PM")
			message_time = datetime.strptime(dt, "%p %H:%M")
			msg.datetime = datetime.combine(message_date ,message_time.timetz())
			msg.contents = log.split("]")[2][1:-1]
			messages.append(msg)
		except :
			pass

# ios
elif info[-6:-2] == ".txt" :
	message_origin = "ios"
	if info[3:23] == "KakaoTalk Chats with" :
		message_origin += "_en"
	else :
		message_origin += "_kr"
	
	#locale kr
	if "kr" in message_origin :
		for log in logs :
			try :
				msg = Msg()
				dt = unicode(log.split(",")[0], 'utf-8')
				dt = dt.replace("오후".decode('utf-8'), "PM")
				dt = dt.replace("오전".decode('utf-8'), "AM")
				msg.datetime = datetime.strptime(dt, '%Y. %m. %d. %p %I:%M')
				msg.sender = log.split(",")[1].split(":")[0][1:-1]
				msg.contents = log.split(",")[1].split(":")[1][1:-1]
				messages.append(msg)
			except :
				print log

	#locale en
	if "en" in message_origin :
		for log in logs :
			try :
				msg = Msg()
				dt = log.split(",")[0]+log.split(",")[1]+log.split(",")[2]
				msg.datetime = datetime.strptime(dt, '%b %d %Y %I:%M %p')
				msg.sender = log.split(",")[3].split(":")[0][1:-1]
				msg.contents = log.split(",")[3].split(":")[1][1:-1]
				messages.append(msg)
			except :
				print log

	
# android
else :
	message_origin = "android"
	if info[3:23] == "KakaoTalk Chats with" :
		message_origin += "_en"
	else :
		message_origin += "_kr"
	
	#locale kr
	if "kr" in message_origin :
		for log in logs :
			try :
				msg = Msg()
				dt = unicode(log.split(",")[0], 'utf-8')
				dt = dt.replace("오후".decode('utf-8'), "PM")
				dt = dt.replace("오전".decode('utf-8'), "AM")
				dt = dt.replace("년".decode('utf-8'), "")
				dt = dt.replace("월".decode('utf-8'), "")
				dt = dt.replace("일".decode('utf-8'), "")
				msg.datetime = datetime.strptime(dt, '%Y %m %d %p %I:%M')
				msg.sender = log.split(",")[1].split(":")[0][1:-1]
				msg.contents = log.split(",")[1].split(":")[1][1:-1]
				messages.append(msg)
			except :
				pass
				#print log

	#locale en
	if "en" in message_origin :
		for log in logs :
			try :
				msg = Msg()
				dt = log.split(",")[0] + log.split(",")[1] + log.split(",")[2]
				msg.datetime = datetime.strptime(dt, '%I:%M%p %B %d %Y')
				msg.sender = log.split(",")[3].split(":")[0][1:-1]
				msg.contents = log.split(",")[3].split(":")[1][1:-1]
				messages.append(msg)
			except :
				print log

for message in messages :
	pass
	print str(message.datetime) + "\t" + message.sender + "\t" + message.contents

print message_origin