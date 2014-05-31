#coding=utf8
import urllib2
import json
import hashlib
import time
from django.views.generic import DeleteView
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
from .utils import (judge_text, to_unicode, user_info_add, music_reply,
                    judge_event, weixin_message_add, judge_voice)
from .models import UserInfo,Tip

TOKEN = getattr(
    settings,
    "WEIXIN_TOKEN",
    "weixin"
)

APPID = "wx07f2f4b7e8caa67a"
SECRET = "bddc99ccda0d85ea18d7b3ea3cc18d3d"


def check_signature(request):
    """本功能用于首次的签名验证，首次验证签名功能后即可注释掉"""
    global TOKEN
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr", None)

    token = TOKEN
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr, content_type="text/plain")
    else:
        return HttpResponse('none', content_type="text/plain")


@csrf_exempt
def index(request):
    if request.method == "GET":
        return check_signature(request)
    if request.method == "POST":
        content = response_msg(request)
        return HttpResponse(content, content_type="application/xml")


def parse_msg(request):
    """此函数用于解析XML文档，确定XML的类型"""
    msg = {}
    xlm_tree = request.body
    root = ET.fromstring(xlm_tree)
    for child in root:
        msg[child.tag] = to_unicode(child.text)
    user_info_add(msg)
    weixin_message_add(msg, xlm_tree)

    return msg


def response_msg(request):
    msg = parse_msg(request)
    # print msg
    if msg['MsgType'] == 'text':
        return judge_text(msg)
    elif msg['MsgType'] == 'music':
        response_content = dict(content=judge_text(msg),
                                touser=msg['FromUserName'],
                                fromuser=msg['ToUserName'],
                                createtime=str(int(time.time())), )
        return music_reply.format(**response_content)

    elif msg['MsgType'] == 'event':
        return judge_event(msg)

    elif msg['MsgType'] == 'voice':
        return judge_voice(msg)


def response_oauth(request):
    code = request.GET.get('code', None)
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
        APPID, SECRET, code)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = json.loads(response.read())
    access_token = content["access_token"]
    openid = content["openid"]
    url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (access_token, openid)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = json.loads(response.read())
    try:
        UserInfo.objects.get(openid=openid, status=1)
    except Exception, e:
        try:
            user_info = UserInfo.objects.get(openid=openid)
            user_info.status = 1
            user_info.nickname = content["nickname"]
            user_info.heading_url = content["headimgurl"]
            user_info.sex = content["sex"]
            user_info.save()
        except Exception, e:
            UserInfo.objects.create(openid=openid, nickname=content["nickname"], sex=content["sex"],
                                    heading_url=content["headimgurl"])
    return HttpResponse("获取用户信息~")


class TipDetailView(DeleteView):
    model = Tip
    template_name = 'weixin/tip_detail.html'