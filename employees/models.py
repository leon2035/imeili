# -*- coding: utf8 -*-
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,User
)
from django.utils import timezone
from django.core.urlresolvers import reverse
from .validators import phone, id_card, tel

class EmployeeManager(BaseUserManager):
    def create_user(self, phone, id_card, password=None):
        if not phone:
            raise ValueError(u'你必须输入一个合法的手机号码')

        user = self.model(
            phone=phone,
            id_card=id_card,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, id_card, password):
        user = self.create_user(
            phone=phone,
            id_card=id_card,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class EmployeePosition(models.Model):
    name = models.CharField(verbose_name=u'职位名称', max_length=30)
    basic_salary = models.DecimalField(verbose_name='底薪', max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'员工职位'
        verbose_name_plural=verbose_name


class Employee(AbstractBaseUser, PermissionsMixin):
    #账户信息
    is_active = models.BooleanField(verbose_name=u'激活', default=True)
    is_staff = models.BooleanField(verbose_name=u'正式员工', default=True)
    #个人信息
    name = models.CharField(verbose_name=u'姓名', max_length=12)
    id_card = models.CharField(verbose_name=u'身份证',
                               max_length=18,
                               unique=True,
                               validators=[id_card],
                               error_messages={'invalid': '身份证号码有误，请重新输入', },
                               help_text='请输入真实的18位身份证号码')
    position = models.ForeignKey(EmployeePosition, verbose_name=u'职位')
    #联系方式
    email = models.EmailField(verbose_name=u'邮箱', max_length=255)
    phone = models.CharField(verbose_name=u'手机',
                             max_length=11,
                             unique=True,
                             validators=[phone],
                             error_messages={'invalid': '手机号码有误，请重新输入', })

    tel = models.CharField(verbose_name=u'固话',
                           max_length=12,
                           validators=[tel],
                           error_messages={'invalid': '固话号码有误，请重新输入', },
                           help_text='格式为：区号-固话号')
    address = models.CharField(verbose_name=u'地址', max_length=255)

    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)

    objects = EmployeeManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['id_card']


    def is_new(self):
        return self.username == ""

    is_new.boolean = True
    is_new.short_description = u"新用户"

    # @property
    def sex(self):
        return u"女" if int(self.id_card[-2]) % 2 == 0 else u'男'

    sex.short_description=u'性别'

    # @property
    def birthday(self):
        return self.id_card[6:14]

    birthday.short_description=u'生日'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.position_id = 1
        super(Employee, self).save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse('employee_detail',kwargs={'pk':self.pk})

    class Meta:
        verbose_name = u'员工'
        verbose_name_plural = verbose_name