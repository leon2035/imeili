#-*-coding:utf8-*-
from django.db import models
from products.models import Product
from employees.models import Employee
from members.models import Member


class MyCart(models.Model):
    seller = models.ForeignKey(Employee)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)



class Order(models.Model):
    cart = models.ForeignKey(MyCart)
    member = models.ForeignKey(Member)
    created_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'订单'
        verbose_name_plural = verbose_name


class LineItem(models.Model):
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()


class Cart(object):
    def __init__(self, *args, **kwargs):
        self.items = []
        self.total_price = 0

    def add_product(self, product):
        self.total_price += product.unit_price
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += 1
                return
        self.items.append(LineItem(product=product, unit_price=product.unit_price, quantity=1))