#coding=utf8
from django.db import models


class UserInfo(models.Model):
    openid = models.CharField('OPENID', max_length=255, unique=True)
    nickname = models.CharField('昵称', max_length=400, blank=True)
    sex = models.CharField('性别', max_length=1, choices=(
        ('1', '男'),
        ('2', '女'),
        ('0', '未知'),
    ))
    heading_url = models.URLField('头像地址')
    status = models.BooleanField('是否激活', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __unicode__(self):
        return self.openid

    class Meta:
        db_table = 'weixin_user'
        verbose_name = u'微信账户'
        verbose_name_plural = verbose_name


class Message(models.Model):
    user = models.ForeignKey(UserInfo, to_field='openid')
    message = models.TextField('用户发送的信息')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = u'weixin_message'
        verbose_name = u'消息'
        verbose_name_plural = verbose_name


class Tip(models.Model):
    title = models.CharField(verbose_name=u'标题',max_length=255)
    description = models.TextField(verbose_name='内容')
    pic_url = models.URLField(verbose_name=u'图片地址')
    url = models.URLField(verbose_name=u'详情地址')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"美丽贴士"
        verbose_name_plural = verbose_name


class Discount(models.Model):
    title = models.CharField(verbose_name=u'标题',max_length=255)
    description = models.TextField(verbose_name=u'促销信息')
    pic_url = models.URLField(verbose_name=u'图片地址')
    url = models.URLField(verbose_name=u'活动详情')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"天天特价"
        verbose_name_plural = verbose_name


class FeedBack(models.Model):
    from_username = models.CharField(u'会员名',max_length=255)
    message = models.CharField(verbose_name=u'反馈内容',max_length=255)
    is_replied = models.BooleanField(verbose_name=u'已回复',default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message

    class Meta:
        verbose_name = u'反馈'
        verbose_name_plural = verbose_name