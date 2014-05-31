# -*- coding: utf8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import Employee,EmployeePosition


class EmployeeAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('name', 'email', 'phone', 'tel', 'address','is_staff','is_active','sex','birthday')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        (u'个人信息', {'fields': ('name','id_card', 'email', 'phone', 'tel', 'address')}),
        (u'权限', {'fields': (('is_staff','is_active','user_permissions'),)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()

class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('name','basic_salary')

admin.site.register(Permission)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeePosition,EmployeePositionAdmin)
admin.site.unregister(Group)