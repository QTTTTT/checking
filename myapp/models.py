# coding=utf8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=64)
    identity = models.CharField(max_length=16, unique=True)
    sex = models.CharField(max_length=16)
    department = models.ForeignKey(Department)

    def __unicode__(self):
        return self.department.name + u'的' + self.name


class Record(models.Model):
    """
    date: 日期
    first_time: 签到
    second_time: 签离
    first_result: 是否迟到
    second_result: 是否早退
    """
    date = models.DateField()
    first_time = models.TimeField(blank=True, null=True)
    second_time = models.TimeField(blank=True, null=True)
    first_result = models.BooleanField(default=False)
    second_result = models.BooleanField(default=False)
    member = models.ForeignKey(Member)

    def __unicode__(self):
        return self.member.name + u'的' + unicode(self.date) + u'签到情况'


class AdminObject(models.Model):
    """
    member: 员工
    late_times: 迟到次数
    early_times: 早退次数
    up_days: 出勤天数
    down_days: 缺勤天数
    """
    member = models.ForeignKey(Member)
    late_times = models.IntegerField(default=0)
    early_times = models.IntegerField(default=0)
    up_days = models.IntegerField(default=0)
    down_days = models.IntegerField(default=0)

    def __unicode__(self):
        return self.member.name + u'的总体出勤情况'


class UserObject(models.Model):
    date = models.DateField()
    up = models.BooleanField(default=False)
    member = models.ForeignKey(Member)
    record = models.ForeignKey(Record, blank=True, null=True)

    def __unicode__(self):
        return self.member.name + u'的' + unicode(self.date) + u'出勤情况'
