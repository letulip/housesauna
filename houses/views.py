from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.db import models
from itertools import chain
from .models import House, Sauna, Project, Category

METATAGS = {
    'house': {
        'title': 'Строительство домов из клееного бруса под ключ в Москве и области — проекты и цены',
        'description': ('Мы строим деревянные дома из клееного бруса для'
                        ' постояного проживания и делаем это качественно.'
                        ' Подберем для вас готовый проект или разработаем индивидуальный.'),
    },
    'sauna': {
        'title': 'Строительство бань из клееного бруса под ключ в Москве и области — проекты и цены',
        'description': ('Мы строим бани из клееного бруса и делаем это качественно. '
                        'Подберем для вас готовый проект или разработаем индивидуальный.'),
    }
}


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'structure-index.html'
    context_object_name = 'all_structures'

    def get_object_count(self, model: models.Model) -> models.Model:
        return model.objects.all().count()

    def get_object_list(self, model: models.Model) -> models.Model:
        return model.objects.filter(pub_date__lte=timezone.now())

    def get_object_dir_name(self, model: models.Model) -> models.Model:
        obj = model.objects.first()
        return obj.dir_name if obj else None

    def get_queryset(self) -> list:
        result_list = list(
            chain(
                # self.get_object_list(House),
                # self.get_object_list(Sauna),
                self.get_object_list(Project)
            )
        )
        return result_list

    def get_context_data(self, **kwargs: dict) -> object:
        context = super(IndexView, self).get_context_data(**kwargs)
        # context['house_count'] = self.get_object_count(House)
        # context['houses_dir_name'] = self.get_object_dir_name(House)
        # context['houses_list'] = self.get_object_list(House)
        # context['sauna_count'] = self.get_object_count(Sauna)
        # context['saunas_dir_name'] = self.get_object_dir_name(Sauna)
        # context['saunas_list'] = self.get_object_list(Sauna)
        context['projects_count'] = self.get_object_count(Project)
        context['projects_list'] = self.get_object_list(Project)
        # context['categories'] = Category.objects.prefetch_related('saunas', 'houses')
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


class CategorySaunaView(generic.View):
    template_name = "categories.html"

    def get(self, request):
        categories = Category.objects.filter(saunas__isnull=False).distinct()

        context = {
            "categories": categories,
            "saunas_list": Sauna.objects.all(),
            "category_title": METATAGS.get('sauna', {}).get('title', ''),
            "category_description": METATAGS.get('sauna', {}).get('description', ''),
        }

        return render(request, self.template_name, context)


class CategoryHousesView(generic.View):
    template_name = "categories.html"

    def get(self, request):
        categories = Category.objects.filter(houses__isnull=False).distinct()

        context = {
            "categories": categories,
            "houses_list": House.objects.all(),
            "category_title": METATAGS.get('house', {}).get('title', ''),
            "category_description": METATAGS.get('house', {}).get('description', '')
        }

        return render(request, self.template_name, context)


class SubcategoriesHousesView(generic.View):
    template_name = "structure-index.html"
    category_template_name = "categories.html"

    def get(self, request, cat_slug, sub_slug=None):
        category = Category.objects.get(slug=cat_slug)
        houses = House.objects.filter(category=category)

        if sub_slug:
            subcategory = Category.objects.get(slug=sub_slug)
            header = subcategory.subcategories_description.get(cat_slug, {}).get('header')
            title = subcategory.subcategories_description.get(cat_slug, {}).get('title')
            description = subcategory.subcategories_description.get(cat_slug, {}).get('description')
            houses = houses.filter(category=subcategory)
        else:
            header = category.header_house
            title = category.title_house
            description = category.description_house

        context = {
            "houses_list": houses,
            "category_description": description,
            "category_title": title,
            "category_header": header
        }

        if subcategories := category.subcategory.all():
            context.update(
                {
                    "categories": subcategories,
                    "curr_category": category,
                }
            )

        template = self.category_template_name if subcategories and not sub_slug else self.template_name

        return render(request, template, context)


class SubcategoriesSaunasView(generic.View):
    template_name = "structure-index.html"
    category_template_name = "categories.html"

    def get(self, request, cat_slug, sub_slug=None):
        category = Category.objects.get(slug=cat_slug)
        saunas = Sauna.objects.filter(category=category)

        if sub_slug:
            subcategory = Category.objects.get(slug=sub_slug)
            saunas = saunas.filter(category=subcategory)

        context = {
            "saunas_list": saunas,
            "category_description": category.description_sauna,
            "category_title": category.title_sauna,
            "category_header": category.header_sauna
        }
        if subcategories := category.subcategory.all():
            context.update(
                {
                    "categories": subcategories,
                    "curr_category": category,
                }
            )

        template = self.category_template_name if subcategories and not sub_slug else self.template_name

        return render(request, template, context)


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
