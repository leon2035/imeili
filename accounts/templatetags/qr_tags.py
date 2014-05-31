# coding: utf-8
from django import template

import qrcode
import cStringIO

register = template.Library()


def object_to_qr_image64(obj, version, box_size, border):
    output = cStringIO.StringIO()
    qr = qrcode.QRCode(version=version, box_size=box_size, border=border)
    if not isinstance(obj, str):
        obj = str(obj)
    qr.add_data(obj)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(output, 'png')
    base64_image = "data:image/png;base64,%s" % output.getvalue().encode(
        'base64')
    return base64_image


@register.inclusion_tag('qrcode/qr_tag.html', takes_context=True)
def qr_from_text(context, text, box_size=5, border=2, version=4):
    base64_image = object_to_qr_image64(text, version, box_size, border)
    return {'qr': base64_image}


@register.inclusion_tag('qrcode/qr_tag.html', takes_context=True)
def qr_from_mail(context, text, box_size=5, border=2, version=4):
    return qr_from_text(context, text='mailto:%s' % text, box_size=box_size, border=border, version=version)


@register.inclusion_tag('qrcode/qr_tag.html', takes_context=True)
def qr_from_contact(context, contact, box_size=5, border=2, version=4):
    qr_text = 'MECARD:'

    for k, v in contact.items():
        if k == 'name':
            qr_text += 'N:%s;' % v.replace(' ', ',')
        elif k == 'sound':
            qr_text += 'SOUND:%s;' % v
        elif k == 'tel':
            if isinstance(k, basestring):
                qr_text += 'TEL:%s;' % v
            else:
                for t in v:
                    qr_text += 'TEL:%s;' % t
        elif k == 'tel-av':
            qr_text += 'TEL-AV:%s;' % v
        elif k == 'email':
            qr_text += 'EMAIL:%s;' % v
        elif k == 'note':
            qr_text += 'NOTE:%s;' % v
        elif k == 'bday':
            qr_text += 'BDAY:%s;' % v
        elif k == 'adr':
            qr_text += 'ADR:%s;' % v
        elif k == 'url':
            qr_text += 'URL:%s;' % v
        elif k == 'nick':
            qr_text += 'NICKNAME:%s;' % v

    return qr_from_text(context, text=qr_text, box_size=box_size, border=border, version=version)
