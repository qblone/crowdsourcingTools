from django import forms

class SubmitMturkFormNB(forms.Form):
    prefix = 'mturknobonusform'
    def clean(self):
        cleaned_data = super(SubmitMturkFormNB, self).clean()
        return cleaned_data
