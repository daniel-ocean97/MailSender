from django import forms

from .models import Client, Letter, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ["theme", "text"]


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["status", "message", "clients"]
        widgets = {
            "clients": forms.CheckboxSelectMultiple,
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Фильтруем клиентов только для текущего пользователя
            if user.has_perm("mail.can_view_all_list"):
                # Если у пользователя есть права на просмотр всех списков, показываем всех клиентов
                self.fields['clients'].queryset = Client.objects.all()
            else:
                # Иначе показываем только клиентов текущего пользователя
                self.fields['clients'].queryset = Client.objects.filter(owner=user)
            
            # Также фильтруем письма
            if user.has_perm("mail.can_view_all_list"):
                self.fields['message'].queryset = Letter.objects.all()
            else:
                self.fields['message'].queryset = Letter.objects.filter(owner=user)
