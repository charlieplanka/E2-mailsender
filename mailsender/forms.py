from django import forms

from .models import Mail


class SendMailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('address', 'text', 'timeout')
        labels = {'address': 'E-mail', 'text': 'Текст письма', 'timeout': 'Сколько ждать до отправки (в секундах)'}
