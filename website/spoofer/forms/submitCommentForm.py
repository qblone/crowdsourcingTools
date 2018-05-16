from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

    
class SubmitCommentsForm(forms.Form):
    comments= forms.CharField (required=False)
    prefix = 'bform_pre'

    def clean_comments(self):
        data = self.cleaned_data['comments']
             # Remember to always return the cleaned data.
        return data
