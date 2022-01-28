from django.http.response import HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.core.mail import send_mail
from itertools import chain
from django.db import models
from houses.models import House, Sauna
from .forms import SubmitFormHandler
from .utility import send_telegram

LAST_TO_VIEW = 6


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'recent_projects'

    def get_object_list(self, model: models.Model) -> models.Model:
        return model.objects.filter(
            pub_date__lte=timezone.now()
        )[:LAST_TO_VIEW]

    def get_queryset(self) -> list:
        chain_list = list(chain(
            self.get_object_list(House),
            self.get_object_list(Sauna)
        ))
        result_list = sorted(
            chain_list,
            key=lambda instance: instance.pub_date,
            reverse=True
        )[:LAST_TO_VIEW]
        return result_list


def submit_form(request: HttpRequest) -> render:

    if request.POST:
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
            Страница объекта: %s''' % (
                form_client,
                form_object,
                form_phone,
                form_email,
                form_page
            )
            sender = 'noreply@domizkleenogobrusa.ru'

            recipients = ['ivladimirskiy@ya.ru']
            send_mail(
                subject,
                message,
                sender,
                recipients
            )
            send_telegram(message)

            return HttpResponseRedirect(request.path_info)

    return render(request, 'submit.html')


def about(request: HttpRequest) -> render:
    return render(request, 'about.html')


def design(request: HttpRequest) -> render:
    return render(request, 'design.html')


def policy(request: HttpRequest) -> render:
    return render(request, 'policy.html')


def production(request: HttpRequest) -> render:
    return render(request, 'production.html')


def notfound(request: HttpRequest) -> render:
    return render(request, '404.html')


def handler404(request: HttpRequest, exception) -> render:
    context = {
        'exeption': exception,
    }
    return render(request, '404.html', context)


def handler500(request: HttpRequest, exception) -> render:
    context = {
        'exeption': exception,
    }
    return render(request, '500.html', context)
