# -*- coding: utf8 -*-
from django.conf.urls import patterns, url
from .views import EmployeeDetailView

urlpatterns = patterns('',
                       url(r'^(?P<pk>\d+)/$', EmployeeDetailView.as_view(), name='employee_detail'),
)
