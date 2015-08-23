# -*- coding: utf8 -*-

import sys
from konlpy.tag import Twitter
from datetime import datetime, timedelta

class Msg:
	def __init__(self):
		datetime = ""
		sender = ""
		contents = ""

def td_increment (dic, key1, key2, value) :
	if key1 not in dic :
		dic[key1] = {}
	if key2 not in dic[key1] :
		dic[key1][key2] = 0
	
	dic[key1][key2] = dic[key1][key2] + value

def increment ( dic, key, value) :
	if key in dic :
		dic[key] = dic[key] + value
	else :
		dic[key] = value

def is_msg_content ( msg_content ) :
	ignore_contents = ['(사진)', '(Photo)', '(photo)', '<Photo>', '<사진>', 'photo', '사진', '(이모티콘)', '(emoticon)', '(Emoticon)']	
	for ignore_content in ignore_contents :
		if ignore_content.decode('utf-8') == msg_content :
			return False
	return True


def normalize( log_file ) :
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
				msg.contents = log.split(",")[2][1:-2].decode('utf-8')
				messages.append(msg)
			except :
				pass
				#print log

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
			except:
				pass

			#window en
			try :
				msg = Msg()
				msg.sender = log.split("]")[0][1:]
				message_time = datetime.strptime(log.split("]")[1][2:], "%H:%M %p")
				msg.datetime = datetime.combine(message_date ,message_time.timetz())
				msg.contents = log.split("]")[2][1:-1].decode('utf-8')
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
				msg.contents = log.split("]")[2][1:-1].decode('utf-8')
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
					msg.contents = log.split(",")[1].split(":")[1][1:-1].decode('utf-8')
					messages.append(msg)
				except :
					pass
					# print log

		#locale en
		if "en" in message_origin :
			for log in logs :
				try :
					msg = Msg()
					dt = log.split(",")[0]+log.split(",")[1]+log.split(",")[2]
					msg.datetime = datetime.strptime(dt, '%b %d %Y %I:%M %p')
					msg.sender = log.split(",")[3].split(":")[0][1:-1]
					msg.contents = log.split(",")[3].split(":")[1][1:-1].decode('utf-8')
					messages.append(msg)
				except :
					pass
					#print log

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
					msg.contents = log.split(",")[1].split(":")[1][1:-1].decode('utf-8')
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
					msg.contents = log.split(",")[3].split(":")[1][1:-1].decode('utf-8')
					messages.append(msg)
				except :
					# print log
					pass

	return messages

def analyzer( messages ) :

	# store senders in chat room
	sender_list = set()

	send_ratio = {}
	msg_bytes = {}
	sent_time = {}
	for i in range (0, 7) :
		sent_time[ i ] = {}
		for j in range(0,24) :
			sent_time[ i ][ j ] = 0	

	kcount = {}
	keywords = {}
	sent_month = ""
	temp_keywords = []

	emoticons = 0
	total = 0
	last_sender = ""

	

	intimacy = {}

	twitter = Twitter()

	for msg in messages :
		
		sender_list.add(msg.sender)

		# to calculate intimacy between member
		if len(last_sender) == 0 :
			last_sender = msg.sender
		if last_sender != msg.sender :
			td_increment( intimacy, last_sender, msg.sender, 1)
			td_increment( intimacy, msg.sender, last_sender, 1)
			last_sender = msg.sender

		# check send ratio.
		td_increment(send_ratio, str(msg.datetime)[:7], msg.sender, 1)

		# calculate msg bytes by sender
		td_increment(msg_bytes, str(msg.datetime)[:7], msg.sender, len(msg.contents))
		
		# count k in msg.
		increment(kcount, msg.sender, msg.contents.count(unicode('ㅋ','utf-8')))

		# count emoticons
		if "(emoticon)" in msg.contents or unicode('(이모티콘)', 'utf-8') in msg.contents:
			emoticons = emoticons + 1

		# calculate active time
		td_increment(sent_time, msg.datetime.weekday() , msg.datetime.time().hour, 1)

		# analyze keyword
		if ( is_msg_content(msg.contents) ) :
			if len(sent_month) == 0 :
				sent_month = str(msg.datetime)[:7]
			elif sent_month == str(msg.datetime)[:7] :
				temp_keywords.append(msg.contents)
			elif sent_month != str(msg.datetime)[:7] :
				keywords_list = twitter.nouns(msg.contents)
				for keyword in keywords_list :
					if len(keyword) > 1:
						td_increment(keywords, sent_month, keyword, 1)
				sent_month = str(msg.datetime)[:7]
				del temp_keywords[:]
				temp_keywords.append(msg.contents)

	# in case of 1:1 chat room
	if len(sender_list) == 2 :
		response_time = {}
		last_sender = ""
		last_response_time = timedelta(0)

		for sender in sender_list :
			response_time[sender] = []
		for msg in messages :
			if len(last_sender) == 0 :
				last_sender = msg.sender
			if last_sender != msg.sender :
				last_sender = msg.sender
				response_time[msg.sender].append(msg.datetime - last_response_time)

			last_response_time = msg.datetime


	print "Who sent how much messages? "

	for date in send_ratio :
		print "in " + str(date)
		for sender in send_ratio[date] :
			print str(sender) + " sent " + str(send_ratio[date][sender]) + " messages"
			total = total + int(send_ratio[date][sender])

	print ""

	print "Msg bytes : "

	for date in msg_bytes :
		print "in " + str(date)
		for sender in msg_bytes[date] :
			print str(sender) + " sent " + str(msg_bytes[date][sender]) + " bytes"

	print ""

	for sender in kcount :
		print sender + " wrote " + unicode('ㅋ','utf-8').encode('utf-8') + " " + str(kcount[sender]) + " byte times"

	print ""

	print ""


	# sorted keywords has 'list' type. not dict.
	print "Top 20 most frequently used keywords in your chatroom."
	for date in keywords :
		print "in " + date
 		sorted_keywords = sorted(keywords[date].items(), key=lambda x:x[1], reverse = True)
		for i in range(0,20) :
			try :
				print sorted_keywords[i][0] + " : " + str(sorted_keywords[i][1])
			except :
				pass

	print ""


	print "When is the most active moment in this chat room?"
	for week in sent_time :
		print week
		for hour in sorted(sent_time[week]):
			print str(sent_time[week][hour]) + " messages were sent at " + str(hour) + " o'clock"
		
	print ""

	print "you guys used emoticons " + str(emoticons) + " times"

	print ""

	print "intimacy between members"

	if len(sender_list) == 2 : 
		for sender in response_time : 
			print sender
			rt_average = sum(response_time[sender], timedelta()) / len(response_time[sender])
			print "responded in " + str(rt_average) + "in average"

	else : 
		for member in intimacy :
			print member + " : "
			for friends in intimacy[member] :
				print " - " + friends + " " + str(intimacy[member][friends])

	print ""

	print "totally, " + str(total) + " messages were sent"

def main () :
	log_file = open(sys.argv[1] , 'r')
	messages = normalize( log_file )
	log_file.close()

	analyzer( messages )

	"""
	for message in messages :
		print str(message.datetime) + "\t" + message.sender + "\t" + message.contents.encode('utf-8')	
	"""

if __name__ == '__main__' :
	main()


			




