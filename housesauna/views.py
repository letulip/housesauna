from typing import Generic
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from houses.models import House, Sauna
from itertools import chain

# Create your views here.
class IndexView(generic.ListView):
  template_name = 'index.html'
  context_object_name = 'recent_projects'
  
  def get_object_list(self, model):
    return model.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:6]

  def get_queryset(self):
    result_list = list(chain(self.get_object_list(House), self.get_object_list(Sauna)))[:6]
    return result_list

def index(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

def design(request):
  return render(request, 'design.html')

def production(request):
  return render(request, 'production.html')

def notfound(request):
  return render(request, '404.html')

def handler404(request, exception, template_name="404.html"):
  return render(request, '404.html')

def handler500(request, exception, template_name="500.html"):
  return render(request, '500.html')
