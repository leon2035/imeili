#coding=utf8
import random
import json
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from rest_framework import generics
from rest_framework.response import Response
from .serializers import LineItemSerializer
from .models import Order, Cart, LineItem,MyCart
from products.models import Product
from weixin.client import Client
from accounts.qrauth.views import uses_redis
from weixin.utils import get_openid
from weixin.models import UserInfo

appid = 'wx07f2f4b7e8caa67a'
appsecret = 'bddc99ccda0d85ea18d7b3ea3cc18d3d'


@login_required
def view_cart(request):
    cart = request.session.get("cart", None)
    t = get_template('cashier/cart.html')
    if not cart:
        cart = Cart()
        request.session["cart"] = cart

    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get("cart", None)
    if not cart:
        cart = Cart()
        request.session["cart"] = cart
    cart.add_product(product)
    request.session['cart'] = cart
    return HttpResponseRedirect(reverse_lazy('view_cart'))


def add_to_discount(request, id):
    product = Product.objects.get(id=id)


def clean_cart(request):
    # request.session['cart'] = Cart()
    mycarts=MyCart.objects.filter(seller=request.user)
    for mycart in mycarts:
        mycart.delete()
    return HttpResponseRedirect(reverse_lazy('view_cart'))



def show_weixin_qrcode(request):
    client = Client(appid=appid, appsecret=appsecret)
    scene_id = random.randint(1, 10000)
    request.session['scene_id'] = scene_id
    qr = {"expire_seconds": 1800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
    ticket = client.create_qrcode(qr)
    qr_img = client.show_qrcode(ticket)
    return HttpResponse(qr_img, mimetype='image/jpeg')


def check_qrcode_scanned(request):
    scene_id = request.session['scene_id']
    openid = get_openid(scene_id)
    if openid == None:
        return HttpResponse('0')
    weixin = UserInfo.objects.get(openid=openid)
    request.session['member']=weixin.member
    response_data = {}
    response_data['name'] = weixin.member.name
    response_data['phone'] = weixin.member.phone
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class LineItemAPI(generics.ListCreateAPIView):
    model = LineItem
    serializer_class = LineItemSerializer

    def get(self, request, *args, **kwargs):
        items = request.session['cart'].items
        serializer = LineItemSerializer(items, many=True)
        return Response(serializer.data)

def my_add_to_cart(request,id):
    seller=request.user
    product=Product.objects.get(id=id)
    try:
        mycart=MyCart.objects.get(product=product,seller=seller)
        mycart.quantity+=1
        mycart.save()
    except Exception,e:
        MyCart.objects.create(product=product,seller=seller)
    return HttpResponse('ok')

def my_view_cart(request):
    try:
        mycarts=MyCart.objects.filter(seller=request.user)
        mycart_all=[]
        for mycart in mycarts:
            mycart_dict={}
            mycart_dict['unit_price']=float(mycart.product.unit_price)
            mycart_dict['name']=mycart.product.name
            mycart_dict['quantity']=mycart.quantity
            mycart_all.append(mycart_dict)
        return HttpResponse(json.dumps(mycart_all),content_type="application/json")
    except Exception,e:
        return HttpResponse('null')

def deal_order(request):
    seller=request.user
    mycart=MyCart.objects.filter(seller=seller)
    try:
        member=request.session['member']
        for cart in mycart:
            Order.objects.create(cart=cart,member=member)
        return HttpResponse('ok')
    except Exception,e:
        return HttpResponse('error')