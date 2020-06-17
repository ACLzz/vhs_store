from django import forms
from django.utils.safestring import mark_safe

from string import ascii_letters, digits
from .models import User

from datetime import datetime
from hashlib import sha256
from requests import post
from os import environ

ALLOWED_SYMBOLS = list(ascii_letters)
ALLOWED_SYMBOLS.extend(list(digits))
ALLOWED_SYMBOLS.extend(list(['_', '-', '.']))


class RegistrationForm(forms.Form):
    def is_valid(self):
        super().is_valid()

        self.error = None
        data = self.cleaned_data
        data['g-recaptcha-response'] = self.data['g-recaptcha-response']

        if self.files['avatar'].size > 8000000:
            self.error = "Avatar must be smaller than 8 megabytes."

        elif User.objects.filter(nickname=data['nickname']):
            self.error = "Nickname is already exist."

        for i in list(data['nickname']):
            if i not in ALLOWED_SYMBOLS:
                self.error = "Unallowed symbols in nickname."

        if data['g-recaptcha-response'] == '':
            self.error = 'Invalid CAPTCHA.'
        else:
            cap_data = {
                'secret': environ.get("CAPTCHA_SECRET"),
                'response': data['g-recaptcha-response']
            }

            resp = post('https://www.google.com/recaptcha/api/siteverify', data=cap_data).json()
            if not resp['success']:
                self.error = 'Invalid CAPTCHA.'

        if self.error:
            return False
        """ Hash password """
        self.cleaned_data['password'] = sha256(self.cleaned_data['password'].encode('utf-8')).hexdigest()
        return True

    error = None

    avatar = forms.ImageField(label=mark_safe('Choose your avatar<br />'), required=False)
    nickname = forms.CharField(label='Nickname', min_length=5, max_length=25, required=True)
    first_name = forms.CharField(label='First name', max_length=15, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=30, min_length=8,
                               required=True)

    day = forms.ChoiceField(choices=[[i, i] for i in list(range(1, 32))])
    month = forms.ChoiceField(choices=[[i, i] for i in list(range(1, 13))])
    year = forms.ChoiceField(choices=[[i, i] for i in list(reversed(range(1940, int(datetime.now().strftime("%Y")) + 1)))])


class LoginForm(forms.Form):
    def is_valid(self):
        super().is_valid()

        data = self.cleaned_data
        data['g-recaptcha-response'] = self.data['g-recaptcha-response']

        if data['g-recaptcha-response'] == '':
            print(1)
            self.error = 'Invalid CAPTCHA.'
        else:
            cap_data = {
                'secret': environ.get("CAPTCHA_SECRET"),
                'response': data['g-recaptcha-response']
            }

            resp = post('https://www.google.com/recaptcha/api/siteverify', data=cap_data).json()
            if not resp['success']:
                self.error = 'Invalid CAPTCHA.'

        user = User.objects.filter(nickname=data['nickname'], password=data['password'])
        if user:
            """ Hash password """
            self.cleaned_data['password'] = sha256(self.cleaned_data['password'].encode('utf-8')).hexdigest()
            self.error = "Invalid username or password."

        if self.error:
            return False
        return True

    nickname = forms.CharField(label='Nickname', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True)

    error = None
