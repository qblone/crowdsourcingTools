from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import URLField


    
class SubmitProAForm(forms.Form):
    spoofer_url = URLField()
    participantID = forms.CharField (label='Participant ID:')
    prefix = 'proaform'
    def clean(self):
        cleaned_data = super(SubmitProAForm, self).clean()
        spoofer_url = self.cleaned_data['spoofer_url']
        participantID  = self.cleaned_data['participantID']
        return cleaned_data
