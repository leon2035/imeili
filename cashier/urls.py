# -*- coding: utf8 -*-
from django.conf.urls import patterns, url
from .views import LineItemAPI

urlpatterns = patterns('',
                       url(r'API/cart/items',
                           LineItemAPI.as_view(), ),
)

urlpatterns += patterns('cashier.views',
                        url(r'^$', 'view_cart', name='view_cart'),
                        url(r'^m$', 'my_view_cart', name='my_view_cart'),
                        url(r'add/(?P<id>[^/]+)/$', 'my_add_to_cart', name='add_to_cart'),
                        url(r'clean/', 'clean_cart', name='clean_cart'),
                        url(r'deal/', 'deal_order', name='deal_order'),
                        url(r'qr/$', 'show_weixin_qrcode', name='show_weixin_qrcode'),
                        url(r'qr/check/$', 'check_qrcode_scanned', name='check_qrcode_scanned'),
)