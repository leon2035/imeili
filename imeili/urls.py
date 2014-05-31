from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import index
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', index,name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^qr/',include('accounts.qrauth.urls')),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^weixin/',include('weixin.urls')),
    url(r'^cashier/',include('cashier.urls')),
    url(r'^product/',include('products.urls')),
    url(r'^employee/',include('employees.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)