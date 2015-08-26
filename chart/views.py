# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from upload.models import FrequencyMessage, FrequencyChars, FrequencyTime, FrequencyWord, Intimacy, Chatroom
import datetime
import MySQLdb
import collections
import json
from django.utils.encoding import smart_str, smart_unicode
from django.utils.datastructures import SortedDict

# Create your views here.
def drawChart(request, uid = 'null'):
	#get user data
	try : 
		data = Chatroom.objects.get(uid=uid)
	except : 
		return HttpResponseRedirect("/")
	chatroom_id = data.id
	startDatetime = data.start_datetime
	isOneToOne = data.is_one_to_one	
	#frequency message count, byte , valid month
	todayYear = datetime.datetime.now().year
	todayMonth = datetime.datetime.now().month
       
	#메세지 보낸 모든 사람들을의 이름을 구한다. (안보낸 달의 경우 0을 입력해주기 위해. 
	msg_names = SortedDict()
	for data in FrequencyMessage.objects.filter(chatroom_id=chatroom_id).order_by('-count'):
		msg_names[data.name] = 1

	#frequency message - all month ( ~ 12)
	object_list = []
	for i in range(0,12) :
		year, month = month_sub(todayYear, todayMonth, i)
                year_month = str(year) + "-" + "%02d" % month
                dic_detail = SortedDict()
		for name in msg_names :
			dic_detail[name] = 0
                for data in FrequencyMessage.objects.filter(chatroom_id=chatroom_id, date=year_month).order_by('-count') :
			#return HttpResponse(smart_str(data.name) + " / " + str(data.count))
                        dic_detail[data.name] = data.count
		
		dic = {}
		sorted(dic_detail.values())
		dic['State'] = year_month
		dic['freq'] = dic_detail
		object_list.append(dic)
        jsonFrequencyMessage = json.dumps(object_list)	

        #byte  message - all month ( ~ 12)
        object_list = []
        for i in range(0,12) :
                year, month = month_sub(todayYear, todayMonth, i)
                year_month = str(year) + "-" + "%02d" % month
                dic_detail = SortedDict()
                for name in msg_names :
                        dic_detail[name] = 0
                for data in FrequencyMessage.objects.filter(chatroom_id=chatroom_id, date=year_month).order_by('-bytes') :
                        #return HttpResponse(smart_str(data.name) + " / " + str(data.bytes))
                        dic_detail[data.name] = data.bytes

                dic = {}
                sorted(dic_detail.values())
                dic['State'] = year_month
                dic['freq'] = dic_detail
                object_list.append(dic)
        jsonByteMessage = json.dumps(object_list)

	#frequency each chars 1 - ㅋ
	object_list = []
	for data in FrequencyChars.objects.filter(chatroom_id=chatroom_id).order_by('-count_char_1'):
		dic = collections.defaultdict()
		dic['label'] = data.name
		dic['value'] = data.count_char_1
		object_list.append(dic)
	jsonFrequencyChar1 = json.dumps(object_list)
	
	#frequency each chars 2 - ㅎ
	object_list = []
	for data in FrequencyChars.objects.filter(chatroom_id=chatroom_id).order_by('-count_char_2'):
		dic = collections.defaultdict()
		dic['label'] = data.name
		dic['value'] = data.count_char_2
		object_list.append(dic)
	jsonFrequencyChar2 = json.dumps(object_list)
	
	#frequency each chars 3 - ㅠ
	object_list = []
	for data in FrequencyChars.objects.filter(chatroom_id=chatroom_id).order_by('-count_char_3') :
		dic = collections.defaultdict()
		dic['label'] = data.name
		dic['value'] = data.count_char_3
		object_list.append(dic)
	jsonFrequencyChar3 = json.dumps(object_list)
	
	#frequency words
	object_list = []
	for data in FrequencyWord.objects.filter(chatroom_id=chatroom_id).order_by('-count')[0:20] :
		dic = collections.defaultdict()
		dic['letter'] = data.word
		dic['frequency'] = data.count
		object_list.append(dic)
	jsonFrequencyWord = json.dumps(object_list)
	
	#frequency time
	object_list = []
	for data in FrequencyTime.objects.filter(chatroom_id=chatroom_id):
		dic = collections.defaultdict()
		dic['hour'] = int(data.hour)+1
		dic['day'] = int(data.week+1)
		dic['value'] = data.count
		object_list.append(dic)
	jsonFrequencyTime = json.dumps(object_list)
	
	#intimacy
	dataIntimacy = {}
	for data in Intimacy.objects.filter(chatroom_id=chatroom_id):
		td_increment(dataIntimacy, data.name, data.target, data.count)
	
	object_list = []
	for name in dataIntimacy :
		dic = {}
		dic['name'] = name
		detail_list = []
		for target in dataIntimacy[name] :
			dic_detail = {}
			dic_detail['name'] = target
			dic_detail['note'] = dataIntimacy[name][target]
			detail_list.append(dic_detail)
		dic['children'] = detail_list
		object_list.append(dic)
	jsonIntimacy = json.dumps(object_list)
	



	t = get_template('chart.html')
	html = t.render({
			'uid':uid, 
			'datetime':startDatetime, 
			'jsonFrequencyMessage':jsonFrequencyMessage,
			'jsonByteMessage':jsonByteMessage,
			'jsonFrequencyTime':jsonFrequencyTime,
			'jsonFrequencyWord':jsonFrequencyWord,
			'jsonFrequencyChar1':jsonFrequencyChar1,
			'jsonFrequencyChar2':jsonFrequencyChar2,
			'jsonFrequencyChar3':jsonFrequencyChar3,
			'jsonIntimacy':jsonIntimacy,
			'isOneToOne':isOneToOne}, request)
	return HttpResponse(html)

def td_increment (dic, key1, key2, value) :
	if key1 not in dic :
		dic[key1] = {}
	if key2 not in dic[key1] :
		dic[key1][key2] = 0	
	dic[key1][key2] = dic[key1][key2] + value

def month_sub(year, month, sub_month):
    result_month = 0
    result_year = 0
    if month > (sub_month % 12):
        result_month = month - (sub_month % 12)
        result_year = year - (sub_month / 12)
    else:
        result_month = 12 - (sub_month % 12) + month
        result_year = year - (sub_month / 12 + 1)
    return (result_year, result_month)
