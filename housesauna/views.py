from itertools import chain
import logging
import urllib3
import socket
import smtplib
import os
from datetime import datetime

from django.db.models import CharField, Value, QuerySet
from django.http.response import HttpResponseRedirect, HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.core import serializers
from django.core.mail import send_mail
from django.db import models
from rest_framework import status
from django.conf import settings

from houses.models import House, Sauna
from .forms import SubmitFormHandler
from .utility import (
    send_telegram,
    save_failed_submission,
    send_email_notification
)

logger = logging.getLogger(__name__)

LAST_TO_VIEW = 3


class IndexView(generic.ListView):
    """
    Отображает главную страницу сайта
    с последними опубликованными домами и банями.
    """
    template_name = 'index.html'
    context_object_name = 'recent_projects'

    MODELS_WITH_STRUCTURE = [
        (House, 'house'),
        (Sauna, 'sauna'),
    ]

    def get_object_list(self, model: models.Model, structure: str) -> QuerySet:
        """
        Возвращает ограниченный список объектов указанной модели,
        опубликованных до текущего момента.
        """
        return model.objects.filter(
            pub_date__lte=timezone.now()
        ).annotate(
            structure=Value(
                structure, output_field=CharField()))[:LAST_TO_VIEW]

    def get_queryset(self) -> list:
        """
        Возвращает объединённый и отсортированный список
        объектов из всех моделей в `MODELS_WITH_STRUCTURE`.
        """
        combined = [
            self.get_object_list(model, structure)
            for model, structure in self.MODELS_WITH_STRUCTURE
        ]
        return sorted(
            chain.from_iterable(combined),
            key=lambda instance: instance.pub_date
        )


class ObjectsYMLView(generic.View):
    """
    Представление для генерации XML-файла каталога объектов.
    """
    def get_object_list(self, model: models.Model) -> models.Model:
        return model.objects.filter(
            pub_date__lte=timezone.now()
        )

    def export_to_xml(self) -> list:
        """
        Объединяет и сортирует объекты домов и бань,
        сериализует их в XML и сохраняет в файл.
        Файл при создании будет лежать в media/catalog.xml
        """
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
        output_path = os.path.join(settings.MEDIA_ROOT, 'catalog.xml')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(data)
            logger.info(f'XML успешно записан в {output_path}')
        except Exception as e:
            logger.error(f'Не удалось записать XML: {e}')
        return result_list

    def get(self, request):
        return HttpResponse(self.export_to_xml())


def submit_form(request: HttpRequest) -> render:
    """
    Обрабатывает отправку формы обратной связи:
    сохраняет данные, отправляет на почту и в Telegram.
    """
    if request.method == 'POST':
        form = SubmitFormHandler(request.POST)

        if form.is_valid():
            form_email = form.cleaned_data['email']
            form_client = form.cleaned_data['name']
            form_phone = form.cleaned_data['phone']
            form_page = form.cleaned_data['form_link']
            form_object = form.cleaned_data['form_name']
            subject = f'{form_client} хочет консультацию'
            message = (
                f'{form_client} хочет консультацию по {form_object}.\n'
                f'Телефон: {form_phone}\nEmail: {form_email}\n'
                f'Страница объекта: {form_page}'
            )
            sender = 'noreply@domizkleenogobrusa.ru'
            recipients = ['ivladimirskiy@ya.ru', 'aslanov72@mail.ru']
            failed = False
            try:
                send_telegram(message)
            except Exception:
                failed = True
            try:
                send_email_notification(subject, message, sender, recipients)
            except Exception:
                failed = True
            if failed:
                logger.info('[SUBMIT] Сохраняем неотправленную заявку')
                save_failed_submission({
                    'Имя': form_client,
                    'Email': form_email,
                    'Телефон': form_phone,
                    'Объект': form_object,
                    'Страница': form_page,
                    'Сообщение': message,
                    'Дата/время': datetime.datetime.now().isoformat()
                })
            return HttpResponseRedirect(request.path_info)

    return render(request, 'submit.html')


def about(request: HttpRequest) -> render:
    """Страница «О нас»."""
    return render(request, 'about.html')


def design(request: HttpRequest) -> render:
    """Страница «Проектирование»."""
    return render(request, 'design.html')


def policy(request: HttpRequest) -> render:
    """Страница «Политика конфиденциальности»."""
    return render(request, 'policy.html')


def production(request: HttpRequest) -> render:
    """Страница «Производство»."""
    return render(request, 'production.html')


def notfound(request: HttpRequest) -> render:
    """Кастомная страница 404 (Not Found)."""
    return render(request, '404.html', status=status.HTTP_404_NOT_FOUND)


def handler404(request: HttpRequest, exception) -> render:
    """Обработчик 404 с контекстом исключения."""
    context = {
        'exception': exception,
    }
    return render(
        request,
        '404.html',
        context,
        status=status.HTTP_404_NOT_FOUND
    )


def handler500(request: HttpRequest, exception) -> render:
    """Обработчик 500 (Internal Server Error) с контекстом исключения."""
    context = {
        'exception': exception,
    }
    return render(
        request,
        '500.html',
        context,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
