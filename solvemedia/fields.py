from django.conf import settings
from django import forms
from solvemedia import SolveMedia
from solvemedia.widgets import SolveMediaCaptcha
import sys

class SolveMediaCaptchaField(forms.CharField):
    # allowAlreadyChecked: don't raise an error if the captcha has already been checked
    def __init__(self, *args, **kwargs):
        super(SolveMediaCaptchaField, self).__init__(*args, **kwargs)
        if 'label' not in kwargs:
            self.label = "Solve the puzzle"
        self.required = True
        self.widget = SolveMediaCaptcha()

    def __getRequestIP(self): # wtfhax https://github.com/praekelt/django-recaptcha/blob/master/captcha/fields.py
        f = sys._getframe()
        while f:
            if 'request' in f.f_locals:
                request = f.f_locals['request']
                if request:
                    remoteIP = request.META.get('REMOTE_ADDR', '')
                    return remoteIP
            f = f.f_back

    def clean(self, val):
        super(SolveMediaCaptchaField, self).clean(val['response'])
        sm = SolveMedia(settings.SM_CKEY, settings.SM_VKEY, settings.SM_HKEY)
        result = sm.check_answer(self.__getRequestIP(), val['challenge'], val['response'])
        if not result['is_valid']:
            raise forms.ValidationError("Error: " + result['error'].capitalize())
        return val['response']
