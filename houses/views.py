from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import generic
from django.utils import timezone
from .models import House, Sauna
from django.db import models
from itertools import chain


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'structure-index.html'
    context_object_name = 'all_structures'

    def get_object_count(self, model: models.Model) -> models.Model:
        return model.objects.all().count()

    def get_object_list(self, model: models.Model) -> models.Model:
        return model.objects.filter(pub_date__lte=timezone.now())

    def get_object_dir_name(self, model: models.Model) -> models.Model:
        return model.objects.first().dir_name

    def get_queryset(self) -> list:
        result_list = list(
            chain(
                self.get_object_list(House),
                self.get_object_list(Sauna)
            )
        )
        return result_list

    def get_context_data(self, **kwargs: dict) -> object:
        context = super(IndexView, self).get_context_data(**kwargs)
        context['house_count'] = self.get_object_count(House)
        context['houses_dir_name'] = self.get_object_dir_name(House)
        context['houses_list'] = self.get_object_list(House)
        context['sauna_count'] = self.get_object_count(Sauna)
        context['saunas_dir_name'] = self.get_object_dir_name(Sauna)
        context['saunas_list'] = self.get_object_list(Sauna)
        return context


# Legacy common index function
def index(request: HttpRequest) -> render:
    house_count = House.objects.all().count()
    houses_list = House.objects.all()
    houses_dir_name = House.objects.first().dir_name

    sauna_count = Sauna.objects.all().count()
    saunas_list = Sauna.objects.all()
    saunas_dir_name = Sauna.objects.first().dir_name

    context = {
        'house_count': house_count,
        'sauna_count': sauna_count,
        'houses_list': houses_list,
        'saunas_list': saunas_list,
        'houses_dir_name': houses_dir_name,
        'saunas_dir_name': saunas_dir_name,
    }
    return render(request, 'structure-index.html', context)


class HouseDetailView(generic.DetailView):
    model = House
    template_name = 'structure-detail.html'
    context_object_name = 'structure'

    def get_object(self, queryset=None):
        try:
            return House.objects.filter(
                pub_date__lte=timezone.now()
            ).get(full_name=self.kwargs.get('slug'))
        except House.DoesNotExist:
            raise Http404()


class SaunaDetailView(generic.DetailView):
    model = Sauna
    template_name = 'structure-detail.html'
    context_object_name = 'structure'

    def get_object(self, queryset=None):
        try:
            return Sauna.objects.filter(
                pub_date__lte=timezone.now()
            ).get(full_name=self.kwargs.get('slug'))
        except Sauna.DoesNotExist:
            raise Http404()


# Legacy common detail function
def detail(request: HttpRequest, structure_name: str) -> render:
    house_exists = None

    try:
        House.objects.get(full_name=structure_name)
    except House.DoesNotExist:
        house_exists = False
    else:
        house_exists = True

    sauna_exists = None

    try:
        Sauna.objects.get(full_name=structure_name)
    except Sauna.DoesNotExist:
        sauna_exists = False
    else:
        sauna_exists = True

    structure = ''
    if house_exists:
        structure = House.objects.get(full_name=structure_name)
    elif sauna_exists:
        structure = Sauna.objects.get(full_name=structure_name)
    else:
        structure = None

    if not structure:
        # raise Http404('No such structure')
        return redirect('/not-found/')
    else:
        return render(
            request,
            'structure-detail.html',
            {'structure': structure}
        )
