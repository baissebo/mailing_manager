from mailings.models import Mailing, Client, Message

from django import forms


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['clients', 'message', 'periodicity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].label_from_instance = lambda obj: (obj.subject[:20] + '...') \
            if len(obj.subject) > 20 else obj.subject


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
