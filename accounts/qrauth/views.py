# -*- coding: utf8 -*-
import redis
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .utils import generate_random_string, salted_hash
from django.contrib.auth import login, get_backends
from django.contrib.auth.decorators import login_required
from django.conf import settings
try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

AUTH_QR_CODE_EXPIRATION_TIME = getattr(
    settings,
    "AUTH_QR_CODE_EXPIRATION_TIME",
    300
)

AUTH_QR_CODE_REDIRECT_URL = getattr(
    settings,
    "AUTH_QR_CODE_REDIRECT_URL",
    "/"
)

AUTH_QR_CODE_REDIS_KWARGS = getattr(
    settings,
    "AUTH_QR_CODE_REDIS_KWARGS",
    {}
)

def uses_redis(func):
    def wrapper(*args, **kwargs):
        kwargs["r"] = redis.StrictRedis(**AUTH_QR_CODE_REDIS_KWARGS)
        return func(*args, **kwargs)

    return wrapper

def qr_code_page(request):
    auth_code = generate_random_string(50)
    auth_code_hash = salted_hash(auth_code)
    url = "http://imeilii.duapp.com" + reverse('qr_code_login', args=(auth_code_hash,))
    return render(request, 'accounts/qr.html', {'url': url,'auth_code_hash':auth_code_hash})

@login_required
@uses_redis
def login_view(request, auth_code_hash,r=None):

    r.setex(
        "".join(["qrauth_", auth_code_hash]),
        AUTH_QR_CODE_EXPIRATION_TIME,
        request.user.id
    )
    return HttpResponse('scan ok')


@uses_redis
def qr_check_scan(request, auth_code_hash,r=None):
    redis_key = "".join(["qrauth_", auth_code_hash])
    user_id = r.get(redis_key)

    if user_id==None:
        return HttpResponse("window.code=201;")

    r.delete(redis_key)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect('/')

    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)
    return HttpResponse("window.code=200;window.redirect_uri='http://imeilii.duapp.com/';")