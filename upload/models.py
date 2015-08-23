# coding:utf-8
from django.db import models

# Create your models here.
class Chatroom(models.Model):
    uid = models.CharField(max_length=40)
    start_datetime = models.DateTimeField(auto_now=True)
    complete_datetime = models.DateTimeField(auto_now=True)
    is_one_to_one = models.PositiveIntegerField(default=0)

class FrequencyMessage(models.Model):
    chatroom = models.ForeignKey(Chatroom, default=0)
    name = models.CharField(max_length=30)
    date = models.CharField(max_length=7)
    count = models.PositiveIntegerField(default=0)
    bytes = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return unicode(self.name)

class FrequencyChars(models.Model):
    chatroom = models.ForeignKey(Chatroom, default=0)
    name = models.CharField(max_length=30)
    count_char_1 = models.PositiveIntegerField(default=0)
    count_char_2 = models.PositiveIntegerField(default=0)
    count_char_3 = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return unicode(self.name)

class FrequencyWord(models.Model):
    chatroom = models.ForeignKey(Chatroom, default=0)
    word = models.CharField(max_length=30)
    count = models.IntegerField(default=0)
    def __unicode__(self):
        return unicode(self.word)

class FrequencyWordAll(models.Model):
    word = models.CharField(max_length=30)
    count = models.IntegerField(default=0)
    date = models.CharField(max_length=7)
    def __unicode__(self):
        return unicode(self.word)

class Intimacy(models.Model):
    chatroom = models.ForeignKey(Chatroom, default=0)
    name = models.CharField(max_length=30)
    target = models.CharField(max_length=30)
    count = models.IntegerField(default=0)

class FrequencyTime(models.Model):
    chatroom = models.ForeignKey(Chatroom, default=0)
    week = models.SmallIntegerField(default=0)
    hour = models.SmallIntegerField(default=0)
    count = models.IntegerField(default=0)

