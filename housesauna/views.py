from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
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
