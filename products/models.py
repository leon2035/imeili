#-*-coding:utf8-*-
from django.db import models
from django.core.urlresolvers import reverse

class ProductCategory(models.Model):
    name = models.CharField(verbose_name=u'分类名', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name=u'商品分类'
        verbose_name_plural = verbose_name


class ProductBrand(models.Model):
    name = models.CharField(verbose_name=u'品牌', max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name=u'商品品牌'
        verbose_name_plural = verbose_name


class Product(models.Model):
    name = models.CharField(verbose_name=u'名称', max_length=255)
    is_active = models.BooleanField(verbose_name=u'上架', default=False)
    date_added = models.DateTimeField(verbose_name=u'添加时间', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)
    bar_code = models.IntegerField(verbose_name=u'条形码', max_length=13)
    unit_price = models.DecimalField(verbose_name=u'单价', max_digits=8, decimal_places=2)
    inventory = models.IntegerField(verbose_name=u'库存', max_length=5)
    category = models.ForeignKey(ProductCategory, verbose_name=u'分类')
    brand = models.ForeignKey(ProductBrand, verbose_name=u'品牌')

    def __unicode__(self):
        return self.name

    def get_price(self):
        return self.unit_price

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])

    @property
    def can_be_added_to_cart(self):
        return self.is_active

    class Meta:
        verbose_name=u'商品'
        verbose_name_plural = verbose_name