import re
from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormUniqueEmail
from pages.forms.recaptcha import ReCaptchaField

class RegistrationForm(RegistrationFormUniqueEmail):
    '''
    Allowed UTF8 logins with space, along with a recaptcha field.
    '''

    username = forms.RegexField(regex=r'^[\w\s_\-+@.\[\]]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs={'class': 'required'}),
                                label=u'username')

    def __init__(self, *args, **kwargs):
        remote_ip = kwargs.pop('remote_ip')
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['captcha'] = ReCaptchaField(remote_ip=remote_ip)

class ContactForm(forms.Form):
    staff_member = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.widgets.Textarea)