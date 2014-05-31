# -*- coding: utf8 -*-
from django.conf.urls import patterns, url
from .views import ProductDetailView
urlpatterns = patterns('',
                       url(r'^(?P<pk>\d+)/$',
                           ProductDetailView.as_view(),
                           name='product_detail'),
)