import re

from django import forms

from operations.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        reg_mobile = '^1[3|4|5|7|8][0-9]{9}$'
        reg = re.compile(reg_mobile)
        if reg.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="invalid mobile")
