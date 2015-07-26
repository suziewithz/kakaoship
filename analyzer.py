# -*- coding: utf8 -*-

def increment ( key, dic ) :
	if key in dic :
		dic[key] = dic[key] + 1
	else :
		dic[key] = 1

log_file = open( "kakaotalk.txt" , 'r')

logs = log_file.readlines()

send_ratio = {}
msg_bytes = {}
sent_time = {}
kcount = 0
total = 0

for i in range(0,24) :
	sent_time[i] = 0



for log in logs :
	if "Date Saved" not in log :
		
		start = log.find(",",21) +2
		end = log.find(":",22)
		if (start > 1 and end > 0) :
			# check send ratio.
			sender = log[start:end]
			increment(sender, send_ratio)

			# calculate msg bytes by sender
			if sender in msg_bytes : 
				msg_bytes[sender] = msg_bytes[sender] + len(log[end:])

			else : 
				msg_bytes[sender] = len(log[end+2:-1])

			# count k in msg.
			kstring = log[end+2:-1].decode('utf-8')
			kcount = kcount + kstring.count(unicode('ㅋ','utf-8'))

			# calculate active time
			start = log.find("," , 10) +2
			end = log.find("," , 15)
			middle = log[start:end].find(":")
			if (start > 0 and end > 0 and middle > 0) :
				time = (int(log[start:start+middle]))%12
				if str(log[end-2 : end]) == "PM" :
					time = time + 12
				increment(time, sent_time)


print "Who sent how much messages? "

for sender in send_ratio :
	print str(sender) + "sent " + str(send_ratio[sender]) + " messages"
	total = total + int(send_ratio[sender])

print ""

print "Msg bytes : "

for msg in msg_bytes :
	print str(msg) + "sent " + str(msg_bytes[msg]) + " bytes"

print ""

print "you guys wrote " + unicode('ㅋ','utf-8').encode('utf-8') + " " + str(kcount) + " byte times"

print ""

print "When is the most active moment in this chat room?"
for time in sorted(sent_time) :
	print str(sent_time[time]) + " messages were sent at " + str(time) + " o'clock"
	

print ""
print "totally, " + str(total) + " messages were sent"

