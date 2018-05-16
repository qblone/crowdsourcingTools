import re

from django import forms

from django.core import validators

from django.core.exceptions import ValidationError
from django.forms import URLField


# class MyExtraURLValidator(validators.RegexValidator):
#     def __init__(self, schemes=None, **kwargs):
#         super(MyExtraURLValidator, self).__init__(**kwargs)

#     def __call__(self, value):
#         message = _('It is not a valid URL.')
#         regex = r"(https?:\/\/spoofer\.caida\.org)\/report\.php\?sessionkey=([a-zA-Z0-9]{14})"
#         if not re.match(regex, value):
#             raise ValidationError(self.message, code=self.code)

#         return super().__call__(value)


# class MyURLField(forms.URLField):
#     default_error_messages = {
#         'invalid': _('Enter a valid URL.'),
#     }
#
#     def __init__(self):
#         super(MyURLField, self).__init__()
#
#         # default_validators = [MyExtraURLValidator()]
#         self.default_validators = [MyExtraURLValidator()]
#
#
#         # super(MyURLField,self).default_validators = [MyExtraURLValidator()]
#         # a = super(MyURLField, self)
#         # self.default_validators.append(MyExtraURLValidator)


class SubmitUrlForm(forms.Form):
    error_messages = {
        'Invalid_URL': 'Please enter correct URL'
    }

    #spoofer_url = URLField(validators=[MyExtraURLValidator])
    spoofer_url = URLField()
    prefix = 'aform_pre'
    proa_value = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())


    def clean (self):
        cleaned_data = super(SubmitUrlForm, self).clean()
        spoofer_url = self.cleaned_data['spoofer_url']
        proa_value  = self.cleaned_data['proa_value']


    # def clean_spoofer_url(self):
    #     data = self.cleaned_data['spoofer_url']

    #     regex = r"(https?:\/\/spoofer\.caida\.org)\/report\.php\?sessionkey=([a-zA-Z0-9]{14})"
    #     if not re.match(regex, data):
    #         raise forms.ValidationError(self.error_messages['Invalid_URL'],
    #                                     code='Invalid URL',  # set the error message key

    #                                     )




            # Remember to always return the cleaned data.
        return cleaned_data
