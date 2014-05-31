# -*- coding: utf8 -*-
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect('/qr')