# coding:utf-8
from django.db import models

# Create your models here.
class FrequencyMessage(models.Model):
    uid = models.CharField(max_length=40)
    name = models.CharField(max_length=20)
    date = models.CharField(max_length=7)
    count = models.IntegerField(default=0)
    byte = models.IntegerField(default=0)
    def __unicode__(self):
        return unicode(self.name)

class FrequencyChars(models.Model):
    uid = models.CharField(max_length=40)
    name = models.CharField(max_length=20)
    count_char_1 = models.IntegerField(default=0)
    count_char_2 = models.IntegerField(default=0)
    count_char_3 = models.IntegerField(default=0)
    def __unicode__(self):
        return unicode(self.name)

class FrequencyWord(models.Model):
    uid = models.CharField(max_length=40)
    word = models.CharField(max_length=20)
    count = models.IntegerField(default=0)
    date = models.CharField(max_length=7, null=True)
    def __unicode__(self):
        return unicode(self.word)

class Intimacy(models.Model):
    uid = models.CharField(max_length=40)
    name = models.CharField(max_length=20)
    target = models.CharField(max_length=20)
    count = models.IntegerField(default=0)

class FrequencyTime(models.Model):
    uid = models.CharField(max_length=40)
    week = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

class User(models.Model):
    uid = models.CharField(max_length=40)
    datetime = models.DateTimeField(auto_now=True)
    complete_datetime = models.DateTimeField(auto_now=True, null=True)
