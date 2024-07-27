from django import forms

from mailings.models import Mailing, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['clients', 'message', 'periodicity']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']
