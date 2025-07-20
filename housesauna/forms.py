import re

from django import forms


class SubmitFormHandler(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    form_name = forms.CharField(max_length=200)
    form_link = forms.URLField(max_length=300)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        cleaned = re.sub(r'[^\d+-]', '', phone).replace('+', '').replace('-', '')
        if not cleaned.replace('+', '').replace('-', '').isdigit():
            raise forms.ValidationError('Введите корректный номер телефона из цифр, допускаются + и -.')
        return '+7' + cleaned
