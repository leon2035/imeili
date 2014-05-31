# -*- coding: utf8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.qrauth.views',
    url(r'^$', 'qr_code_page', name='qr_login'),
    url(
        r'^(?P<auth_code_hash>[a-f\d]{40})/$',
        'login_view',
        name='qr_code_login'
    ),
    url(
        r'^c/(?P<auth_code_hash>[a-f\d]{40})/$',
        'qr_check_scan',name='qr_check_scan'
    ),
)