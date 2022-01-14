from django import forms

class SubmitFormHandler(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=100)
    form_name = forms.CharField(max_length=200)
    form_link = forms.URLField(max_length=300)

    # def submit(request):
    #     if request.method == 'POST':
    #           print(request)