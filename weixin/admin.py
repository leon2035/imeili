from django.contrib import admin
from .models import Tip, Discount, UserInfo, FeedBack


class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pic_url', 'url')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pic_url', 'url')


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('openid', 'nickname', 'sex', 'heading_url')


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(FeedBack)
admin.site.register(Tip, TipAdmin)
admin.site.register(Discount, DiscountAdmin)