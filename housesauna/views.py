from urllib.parse import urljoin

from django.db.models import CharField, Value, QuerySet
from django.http.response import HttpResponseRedirect, HttpResponse
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from django.core import serializers
from django.core.files import File
from django.core.mail import send_mail
from django.db import models

from itertools import chain

from houses.models import House, Sauna, Category
from .forms import SubmitFormHandler
from .utility import send_telegram

LAST_TO_VIEW = 3


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'recent_projects'

    def get_object_list(self, model: models.Model, structure: str) -> QuerySet:
        return model.objects.filter(
            pub_date__lte=timezone.now()
        ).annotate(structure=Value(structure, output_field=CharField()))[:LAST_TO_VIEW]

    def get_queryset(self) -> list:
        houses = self.get_object_list(House, 'house')
        saunas = self.get_object_list(Sauna, 'sauna')

        result = sorted(
            chain(list(houses), list(saunas)),
            key=lambda instance: instance.pub_date
        )
        return result


class ObjectsYMLView(generic.View):
    def get_object_list(self, model: models.Model) -> models.Model:
        return model.objects.filter(
            pub_date__lte=timezone.now()
        )

    def export_to_xml(self) -> list:
        chain_list = list(
            chain(
                self.get_object_list(House),
                self.get_object_list(Sauna)
            )
        )
        result_list = sorted(
            chain_list,
            key=lambda instance: instance.pub_date,
            reverse=True
        )
        data = serializers.serialize('xml', result_list)
        f = open('catalog.xml', 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()
        print('Done')
        return result_list

    def get(self, request):
        return HttpResponse(self.export_to_xml())


def submit_form(request: HttpRequest) -> render:

    if request.POST:
        form = SubmitFormHandler(request.POST)

        if form.is_valid():
            form_email = form.cleaned_data['email']
            form_client = form.cleaned_data['name']
            form_phone = form.cleaned_data['phone']
            form_page = form.cleaned_data['form_link']
            form_object = form.cleaned_data['form_name']
            subject = f'{form_client} хочет консультацию'
            message = f'''{form_client} хочет консультацию по {form_object}.
            Телефон: {form_phone}
            Email: {form_email}
            Страница объекта: {form_page}'''
            sender = 'noreply@domizkleenogobrusa.ru'

            send_telegram(message)

            recipients = ['ivladimirskiy@ya.ru', 'aslanov72@mail.ru']
            send_mail(
                subject,
                message,
                sender,
                recipients
            )

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
        'exception': exception,
    }
    return render(request, '404.html', context)


def handler500(request: HttpRequest, exception) -> render:
    context = {
        'exception': exception,
    }
    return render(request, '500.html', context)
