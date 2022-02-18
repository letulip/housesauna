from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.db import models
from itertools import chain
from .models import House, Sauna, Project


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
                self.get_object_list(Sauna),
                self.get_object_list(Project)
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
        context['projects_count'] = self.get_object_count(Project)
        context['projects_list'] = self.get_object_list(Project)
        return context


class HouseDetailView(generic.DetailView):
    model = House
    template_name = 'structure-detail.html'
    context_object_name = 'structure'

    def get_queryset(self):
        self.house = get_object_or_404(
            House, full_name=self.kwargs.get('slug')
        )
        return House.objects.filter(slug=self.house)


class SaunaDetailView(generic.DetailView):
    model = Sauna
    template_name = 'structure-detail.html'
    context_object_name = 'structure'

    def get_queryset(self):
        self.sauna = get_object_or_404(
            Sauna, full_name=self.kwargs.get('slug')
        )
        return Sauna.objects.filter(slug=self.sauna)


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'project-detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        self.project = get_object_or_404(
            Project, slug=self.kwargs.get('slug')
        )
        return Project.objects.filter(full_name=self.project)


# Legacy function for OLD URLs support
def detail(request, structure_name):
    house_exists = ''

    try:
        House.objects.get(full_name=structure_name)
    except House.DoesNotExist:
        house_exists = False
    else:
        house_exists = True

    sauna_exists = ''

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
