from typing import Generic
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from django.core.mail import send_mail
from houses.models import House, Sauna
from itertools import chain
from .forms import SubmitFormHandler

import telepot

my_token = None
# TODO read form file

my_chat_id = None
# TODO read form file

def send_telegram(msg, chat_id=my_chat_id, token=my_token):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    print(msg)
    bot = telepot.Bot(my_token)
    bot.sendMessage(chat_id=chat_id, text=msg)
    # info('message was sent')

# Create your views here.
class IndexView(generic.ListView):
  template_name = 'index.html'
  context_object_name = 'recent_projects'
  
  def get_object_list(self, model):
    return model.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:6]

  def get_queryset(self):
    chain_list = list(chain(self.get_object_list(House), self.get_object_list(Sauna)))
    result_list = sorted(
      chain_list, key=lambda instance: instance.pub_date, reverse=True)[:6]
    return result_list

# def index(request):
#   return render(request, 'index.html')

def submit_form(request):
  if request.method == 'POST':
    form = SubmitFormHandler(request.POST)

    if form.is_valid():
      form_email = form.cleaned_data['email']
      form_client = form.cleaned_data['name']
      form_phone = form.cleaned_data['phone']
      form_page = form.cleaned_data['form_link']
      form_object = form.cleaned_data['form_name']
      subject = '%s хочет консультацию' % (form_client)
      message = '''%s хочет консультацию по %s.
      Телефон: %s
      Email: %s
      Страница объекта: %s''' % (form_client, form_object, form_phone, form_email, form_page)
      sender = 'noreply@domizkleenogobrusa.ru'

      recipients = ['ivladimirskiy@ya.ru']
      # send_mail(subject, message, sender, recipients)
      send_telegram(message)
    
      return HttpResponseRedirect(request.path_info)

  return render(request, 'submit.html')

def about(request):
  return render(request, 'about.html')

def design(request):
  return render(request, 'design.html')

def policy(request):
  return render(request, 'policy.html')

def production(request):
  return render(request, 'production.html')

def notfound(request):
  return render(request, '404.html')

def handler404(request, exception, template_name="404.html"):
  return render(request, '404.html')

def handler500(request, exception, template_name="500.html"):
  return render(request, '500.html')
