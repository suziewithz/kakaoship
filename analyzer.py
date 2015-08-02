# -*- coding: utf8 -*-

import sys
from konlpy.tag import Kkma
import operator

def increment ( dic, key, value) :
	if key in dic :
		dic[key] = dic[key] + value
	else :
		dic[key] = value


log_file = open (sys.argv[1] , 'r')

logs = log_file.readlines()

send_ratio = {}
msg_bytes = {}
sent_time = {}
kcount = {}
keywords = {}
emoticons = 0
total = 0

kkma = Kkma()

for i in range(0,24) :
	sent_time[i] = 0



for log in logs :
	if "Date Saved" not in log :
		
		start = log.find(",",21) +2
		end = log.find(":",22) -1
		if (start > 1 and end > 0) :
			sender = log[start:end]
			msg = log[end+2:-1].decode('utf-8')
			
			# check send ratio.
			increment(send_ratio, sender, 1)

			# calculate msg bytes by sender
			increment(msg_bytes, sender, len(msg))
			
			# count k in msg.
			increment(kcount, sender, msg.count(unicode('ㅋ','utf-8')))

			# count emoticons
			if "(emoticon)" in msg or unicode('(이모티콘)', 'utf-8') in msg:
				emoticons = emoticons + 1

			# calculate active time
			start = log.find("," , 10) +2
			end = log.find("," , 15)
			middle = log[start:end].find(":")

			if (start > 0 and end > 0 and middle > 0) :
				# make it military time. 0~23
				time = (int(log[start:start+middle]))%12
				if str(log[end-2 : end]) == "PM" :
					time = time + 12
				increment(sent_time, time, 1)

			# analyze keyword
			keywords_list = kkma.nouns(msg)
			for keyword in keywords_list :
				increment(keywords, keyword, 1)

log_file.close()

print "Who sent how much messages? "

for sender in send_ratio :
	print str(sender) + " sent " + str(send_ratio[sender]) + " messages"
	total = total + int(send_ratio[sender])

print ""

print "Msg bytes : "

for msg in msg_bytes :
	print str(msg) + " sent " + str(msg_bytes[msg]) + " bytes"

print ""

for sender in kcount :
	print sender+ " wrote " + unicode('ㅋ','utf-8').encode('utf-8') + " " + str(kcount[sender]) + " byte times"

print ""

print ""

# sorted keywords has 'list' type. not dict.
sorted_keywords = sorted(keywords.items(), key=lambda x:x[1], reverse = True)

for i in range(0,20) :
	print sorted_keywords[i][0] + " : " + str(sorted_keywords[i][1])

print ""

print "When is the most active moment in this chat room?"
for time in sorted(sent_time) :
	print str(sent_time[time]) + " messages were sent at " + str(time) + " o'clock"
	
print ""

print "you guys used emoticons " + str(emoticons) + " times"

print ""
print "totally, " + str(total) + " messages were sent"

