# -*- coding: utf8 -*-
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Employee

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='再次输入密码', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="密码",
        help_text=u"原始密码未被保存，无法查看原始密码，"
                    u"可以点击<a href=\"password/\">这里</a>修改密码。")

    class Meta:
        model = Employee
        fields = ('name','email','phone','tel','address')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    username=forms.CharField(label='用户名')
    password=forms.CharField(label='密码')

class RegisterForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields={'password','name','address'}



