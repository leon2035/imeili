#coding=utf8
import re
from .models import UserInfo, Message
import time
from .models import Tip, Discount, FeedBack
from members.models import Member,MemberCard,DEFAULT_MEMBER_LEVEL
from accounts.qrauth.views import uses_redis

text_reply = """
<xml>
<ToUserName><![CDATA[{touser}]]></ToUserName>
<FromUserName><![CDATA[{fromuser}]]></FromUserName>
<CreateTime>{createtime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""

music_reply = """
 <xml>
 <ToUserName><![CDATA[{to}]]></ToUserName>
 <FromUserName><![CDATA[{fromuser}]]></FromUserName>
 <CreateTime>{createtime}</CreateTime>
 <MsgType><![CDATA[music]]></MsgType>
 <Music>
 <Title><![CDATA[{title}]]></Title>
 <Description><![CDATA[{description}]]></Description>
 <MusicUrl><![CDATA[{MUSIC_Url}]]></MusicUrl>
 <HQMusicUrl><![CDATA[{HQ_MUSIC_Url}]]></HQMusicUrl>
 </Music>
 <FuncFlag>0</FuncFlag>
 </xml>
"""
news_text = """
<xml>
    <ToUserName><![CDATA[{to}]]></ToUserName>
    <FromUserName><![CDATA[{fromuser}]]></FromUserName>
    <CreateTime>{createtime}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    {article}
    <FuncFlag>1</FuncFlag>
</xml>
"""


def user_info_add(msg):
    try:
        UserInfo.objects.get(openid=msg['FromUserName'], status=1)
    except Exception, e:
        try:
            user_info = UserInfo.objects.get(openid=msg['FromUserName'])
            user_info.status = 1
            user_info.save()
        except Exception, e:
            user = UserInfo.objects.create(openid=msg['FromUserName'])
            member_card=MemberCard.objects.create(level_id=DEFAULT_MEMBER_LEVEL)
            member=Member.objects.create(weixin=user,card=member_card)



def user_info_del(msg):
    try:
        user_info = UserInfo.objects.get(openid=msg['FromUserName'])
        user_info.status = 0
        user_info.save()
    except Exception, e:
        pass


def weixin_message_add(msg, xml):
    xml = re.sub(r'\n', '', xml)
    try:
        Message.objects.create(user_id=msg['FromUserName'], message=xml)
    except Exception, e:
        pass


def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value


def judge_text(msg):
    """兼容微信4.5一下的版本"""
    if msg['Content'] == 'Hello2BizUser':
        content = u'——尊敬的【爱美丽】会员——\n点击【天天特价】掌握最新优惠活动。\n点击【美丽行动】护肤、美妆、时尚……我们帮您搞定！\n点击【会员中心】补全个人信息，更有豪礼相送！'
        response_content = dict(content=content, touser=msg['FromUserName'], fromuser=msg['ToUserName'],
                                createtime=str(int(time.time())))
        user_info_add(msg)
        return to_unicode(text_reply).format(**response_content)
    elif u"反馈" in msg['Content']:
        content = u'已收到您的反馈，我们将在一个工作日内给你回复。'
        FeedBack.objects.create(from_username=msg['FromUserName'], message=msg['Content'])
        response_content = dict(content=content, touser=msg['FromUserName'], fromuser=msg['ToUserName'],
                                createtime=str(int(time.time())))
        return to_unicode(text_reply).format(**response_content)
    else:
        content = u'尊敬的【爱美丽】会员，我们将竭诚为你提供最优质的服务！如果您对我们有什么意见和建议，请回复#反馈#您想说的话。'
        reply_info = dict(touser=msg['FromUserName'], fromuser=msg['ToUserName'], createtime=str(int(time.time())),
                          content=content)
        return to_unicode(text_reply).format(**reply_info)


def judge_event(msg):
    if msg['Event'] == 'subscribe':
        user_info_add(msg)
        content = u'——尊敬的【爱美丽】会员——\n点击【天天特价】掌握最新优惠活动。\n点击【美丽行动】护肤、美妆、时尚……我们帮您搞定！\n点击【会员中心】补全个人信息，更有豪礼相送！'
        reply_info = dict(touser=msg['FromUserName'], fromuser=msg['ToUserName'], createtime=str(int(time.time())),
                          content=content)
        return to_unicode(text_reply).format(**reply_info)

    elif msg['Event'] == 'unsubscribe':
        user_info_del(msg)

    elif msg['Event'] == 'CLICK':
        event_key = msg['EventKey']
        if event_key == "TODAY_ON_SALE":
            discounts = Discount.objects.all().order_by('-id')[:5]
            items = ''
            for discount in discounts:
                title = discount.title
                description = discount.description
                pic_url = discount.pic_url
                url = discount.url
                items += """<item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                    </item>""" % (title, to_unicode(description), pic_url, url)
            article = """<ArticleCount>%s</ArticleCount>
                        <Articles>
                         %s
                        </Articles> """ % (len(discounts), items)
            send_info = dict(article=to_unicode(article), to=msg['FromUserName'], fromuser=msg['ToUserName'],
                             createtime=str(int(time.time())))
            return to_unicode(news_text).format(**send_info)
        elif event_key == "TIPS":
            tips = Tip.objects.all().order_by('-id')[:5]
            items = ''
            for tip in tips:
                title = tip.title
                description = tip.description
                pic_url = tip.pic_url
                url = tip.url
                items += """<item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                    </item>""" % (title, to_unicode(description), pic_url, url)
            article = """<ArticleCount>%s</ArticleCount>
                        <Articles>
                         %s
                        </Articles> """ % (len(tips), items)
            send_info = dict(article=to_unicode(article), to=msg['FromUserName'], fromuser=msg['ToUserName'],
                             createtime=str(int(time.time())))
            return to_unicode(news_text).format(**send_info)

        elif event_key == "HELP":
            content = u'——尊敬的【爱美丽】会员——\n点击【天天特价】掌握最新优惠活动。\n点击【美丽行动】护肤、美妆、时尚……我们帮您搞定！\n点击【会员中心】补全个人信息，更有豪礼相送！'
            reply_info = dict(touser=msg['FromUserName'], fromuser=msg['ToUserName'], createtime=str(int(time.time())),
                              content=content)
            return to_unicode(text_reply).format(**reply_info)
        else:
            content = u'您已穿越到火星，人类已经无法阻止你了。'
            reply_info = dict(touser=msg['FromUserName'], fromuser=msg['ToUserName'], createtime=str(int(time.time())),
                              content=content)
            return to_unicode(text_reply).format(**reply_info)

    elif msg['Event'] == 'SCAN':
        bound_sceneid_with_openid(msg)
        content = u'欢迎来到收银台。'
        reply_info = dict(touser=msg['FromUserName'], fromuser=msg['ToUserName'], createtime=str(int(time.time())),
                              content=content)
        return to_unicode(text_reply).format(**reply_info)


def judge_voice(msg):
    pass

@uses_redis
def bound_sceneid_with_openid(msg,r=None):
    openid=msg['FromUserName']
    sceneid=msg['EventKey']
    r.setex(sceneid,300,openid)

@uses_redis
def get_openid(sceneid,r=None):
    openid=r.get(str(sceneid))
    if openid == None:
        return
    r.delete(sceneid)
    return openid



