# -*- coding: utf8 -*-
from django.db import models
from weixin.models import UserInfo
from .utils import generate_initial_number_by_year

DEFAULT_MEMBER_LEVEL=1

class MemberLevel(models.Model):
    level_name = models.CharField(verbose_name=u'级别名称', max_length=12)
    upper_limit = models.DecimalField(verbose_name=u'上限',
                                      max_digits=14,
                                      decimal_places=2)
    lower_limit = models.DecimalField(verbose_name=u'下限',
                                      max_digits=14,
                                      decimal_places=2)
    discount = models.DecimalField(verbose_name=u'折扣', max_digits=3,
                                   decimal_places=2)

    def __unicode__(self):
        return self.level_name

    class Meta:
        verbose_name = u"会员等级"
        verbose_name_plural = verbose_name


class MemberCard(models.Model):
    card_no = models.AutoField(verbose_name=u'会员卡号', max_length=10,
                               primary_key=True)
    level = models.ForeignKey(MemberLevel,default=DEFAULT_MEMBER_LEVEL)
    sum = models.DecimalField(verbose_name=u'总消费金额', max_digits=3,
                              decimal_places=2, default=0.00)
    remaining_sum = models.DecimalField(verbose_name=u'余额', max_digits=3,
                                        decimal_places=2, default=0.00)
    reg_time = models.DateTimeField(verbose_name=u'注册时间', auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not MemberCard.objects.all():
            self.card_no = generate_initial_number_by_year(0)
        super(MemberCard, self).save(force_insert, force_update, using,
                                     update_fields)

    def __unicode__(self):
        return str(self.card_no)

    class Meta:
        verbose_name = u"会员卡"
        verbose_name_plural = verbose_name


class Member(models.Model):
    weixin = models.OneToOneField(UserInfo, verbose_name=u'微信')
    card = models.OneToOneField(MemberCard, verbose_name=u'会员卡')
    name = models.CharField(verbose_name=u'姓名', max_length=12)
    birthday = models.DateField(verbose_name=u'生日', null=True)
    phone = models.CharField(verbose_name=u'手机', max_length=11)
    address = models.CharField(verbose_name=u'地址', max_length=255)
    job = models.CharField(verbose_name=u'职业', max_length=255)
    income = models.CharField(verbose_name=u'收入水平', choices=(
        ('1', u'2000元以下'),
        ('2', '2000-5000'),
        ('3', '5000-8000'),
        ('4', u'8000元以上'),
    ), max_length=1)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'会员信息'
        verbose_name_plural = verbose_name