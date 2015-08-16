# coding: utf-8
import os
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from konlpy.tag import Twitter
from upload.models import FrequencyMessage, FrequencyChars, FrequencyTime, FrequencyWord, Intimacy, Chatroom
from django.utils import timezone
from analyzer import Msg, td_increment, increment, normalize
from django.utils.encoding import smart_str, smart_unicode
import datetime
import sys
import operator
import uuid

# Create your views here.
def index(request):
    t = get_template('index.html')
    html = t.render(request)
    return HttpResponse(html)

@csrf_exempt
def upload(request):
	if request.method == 'POST':
		if 'file' in request.FILES:
  			myUid = str(uuid.uuid4())

			dataChatroom = Chatroom(
				uid = myUid
			)
			dataChatroom.save()

			data = Chatroom.objects.get(uid=myUid) 
			chatroom_id = data.id

			file = request.FILES['file']
			filename = myUid		
			
			fp = open('%s/%s' % ("data", filename) , 'wb')
			for chunk in file.chunks():
				fp.write(chunk)
			fp.close()
			log_file = open('%s/%s' % ("data", filename) , 'r')
						
			messages = normalize( log_file )
			log_file.close()
			
			#파일 삭제
			os.remove('%s/%s' % ("data", filename))
			
			send_ratio = {}
			msg_bytes = {}
			sent_time = {}
			kcount = {}
			hcount = {}
			ucount = {}
			keywords = {}
			emoticons = 0
			total = 0
			last_sender = ""
			
			intimacy = {}
			
			twitter = Twitter()
		
			for msg in messages :
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
				increment(hcount, msg.sender, msg.contents.count(unicode('ㅎ','utf-8')))
				increment(ucount, msg.sender, msg.contents.count(unicode('ㅠ','utf-8')))
			
				# count emoticons
				if "(emoticon)" in msg.contents or unicode('(이모티콘)', 'utf-8') in msg.contents:
					emoticons = emoticons + 1
			
				# calculate active time
				td_increment(sent_time, msg.datetime.weekday(), msg.datetime.time().hour, 1)
			
				# analyze keyword
				keywords_list = twitter.nouns(msg.contents)
				
				for keyword in keywords_list :
					if len(keyword) > 1:
						td_increment(keywords, str(msg.datetime)[:7], keyword, 1)
		
			#insert frequency message & byte	
			for date in send_ratio :
				for sender in send_ratio[date] :
                                	dataMessage = FrequencyMessage(
                                		chatroom_id = chatroom_id,
						name = unicode(str(sender), 'utf-8').encode('utf-8'),
                                		date = date,
                                		count = int(send_ratio[date][sender]),
						bytes = int(msg_bytes[date][sender])
                        		)
                        		dataMessage.save()
			
			#insert most keywords
			for date in keywords :
				sorted_keywords = sorted(keywords[date].items(), key=lambda x:x[1], reverse = True)
				for i in range(0,len(sorted_keywords)) :
					#try :
						word = smart_str(sorted_keywords[i][0])
						dataWord = FrequencyWord(
                                			chatroom_id = chatroom_id,
							date = date,
							word = word,
							count = int(sorted_keywords[i][1])
						)
						dataWord.save()
					#except :
					#	pass
			
			#insert moment
			for week in sent_time :
				for hour in sent_time[week] :
					dateTime = FrequencyTime(
                                		chatroom_id = chatroom_id,
						week = int(week),
						hour = int(hour),
						count = int(sent_time[week][hour])
					)
					dateTime.save()

			#insert intimacy
			for member in intimacy :
                                for friends in intimacy[member] :
					dataIntimacy = Intimacy(
                                		chatroom_id = chatroom_id,
						name = unicode(str(member), 'utf-8').encode('utf-8'),
						target = unicode(str(friends), 'utf-8').encode('utf-8'),
						count = int(intimacy[member][friends])
					)
                                	dataIntimacy.save()


			#insert each char count
			for sender in kcount :
				dataChar = FrequencyChars(
                                	chatroom_id = chatroom_id,
					name = unicode(str(sender), 'utf-8').encode('utf-8')
                                )
				try :
					dataChar.count_char_1 = int(kcount[sender])
				except :
					pass
				try :
                                        dataChar.count_char_2 = int(hcount[sender])
                                except :
                                        pass
				try :
                                        dataChar.count_char_3 = int(ucount[sender])
                                except :
                                        pass

                                dataChar.save()

			Chatroom.objects.filter(uid=myUid).update(complete_datetime=datetime.datetime.now())
			return HttpResponse(myUid)
	return HttpResponse('Failed to Upload File')
	



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
