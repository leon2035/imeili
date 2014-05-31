from django.conf.urls import patterns, url
from .views import index, response_oauth, TipDetailView

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^oauth/response/$', response_oauth),
                       url(r'^tip/(?P<pk>\d+)/$', TipDetailView.as_view(),
                           name='tip_detail'),
)
