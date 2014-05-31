# -*- coding: utf8 -*-
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_re=re.compile(r'^1[3|4|5|8][0-9]\d{4,8}$')
phone=RegexValidator(phone_re,u'不是完整的11位手机号或者正确的手机号前七位','invalid')

id_card_re=re.compile(r'^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$')
id_card=RegexValidator(id_card_re,u'身份证号码有误','invalid')

tel_re=re.compile(r'^(([0\+]\d{2,3}-)?(0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$')
tel=RegexValidator(tel_re,u'固话号码有误','invalid')
