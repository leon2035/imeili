from django.contrib import admin
from .models import Member,MemberLevel,MemberCard

class MemberLevelAdmin(admin.ModelAdmin):
    list_display = ('level_name','upper_limit','lower_limit','discount')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name','card','phone','address')

admin.site.register(Member,MemberAdmin)
admin.site.register(MemberCard)
admin.site.register(MemberLevel,MemberLevelAdmin)
