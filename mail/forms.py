from django import forms
from .models import Client, Letter, Mailing

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['theme', 'text']

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['end_time', 'status', 'message', 'clients']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'clients': forms.CheckboxSelectMultiple,
        }


