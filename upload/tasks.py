from djcelery import celery
from upload.models import *
from django.utils import timezone
from analyzer import *
from django.utils.encoding import smart_str, smart_unicode
from django.db.models import F, Sum, Count
import collections
import datetime
from datetime import timedelta
import sys
import operator
import uuid
import json


@celery.task(name='tasks.insert_keywords')
def insert_keywords(keyword, date, cnt):
	word = smart_str(keyword)
	getWordData = FrequencyWordAll.objects.filter(word=keyword, date=date)
                                    
	if getWordData.exists() :
		FrequencyWordAll.objects.filter(id=getWordData[0].id).update(count=F('count') + cnt)
	else :
		dataWordAll = FrequencyWordAll(
			date = date,
			word = word,
			count = int(cnt)
		)
		dataWordAll.save()
