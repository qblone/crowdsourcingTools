from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import URLField


    
class SubmitProAFormNB(forms.Form):
    participantID = forms.CharField (label='Participant ID:')
    prefix = 'proanobonusform'
    def clean(self):
        cleaned_data = super(SubmitProAFormNB, self).clean()
        participantID  = self.cleaned_data['participantID']
        return cleaned_data
