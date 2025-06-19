from itertools import chain
import logging

from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.db import models

from .models import House, Sauna, Project, Category

logger = logging.getLogger(__name__)

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


class IndexView(generic.ListView):
    """
    Главная страница, отображающая список всех проектов.
    """
    template_name = 'structure-index.html'
    context_object_name = 'all_structures'

    def get_object_count(self, model: models.Model) -> models.Model:
        """Возвращает количество объектов модели."""
        return model.objects.all().count()

    def get_object_list(self, model: models.Model) -> models.Model:
        """Возвращает объекты модели, опубликованные на текущий момент."""
        return model.objects.filter(pub_date__lte=timezone.now())

    def get_object_dir_name(self, model: models.Model) -> models.Model:
        """Возвращает наименование категории объекта (дом или баня)."""
        obj = model.objects.first()
        return obj.dir_name if obj else None

    def get_queryset(self) -> list:
        """Объединяет все структуры (сейчас только проекты)."""
        result_list = list(
            chain(
                # self.get_object_list(House),
                # self.get_object_list(Sauna),
                self.get_object_list(Project)
            )
        )
        return result_list

    def get_context_data(self, **kwargs: dict) -> object:
        """Добавляет в контекст количество и список проектов."""
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
    """
    Детальная страница дома.
    """
    model = House
    template_name = 'structure-detail.html'
    context_object_name = 'structure'

    def get_queryset(self):
        """Возвращает queryset по slug дома."""
        return House.objects.filter(full_name=self.kwargs.get('slug'))


class SaunaDetailView(generic.DetailView):
    """
    Детальная страница бани.
    """
    model = Sauna
    template_name = 'structure-detail.html'
    context_object_name = 'structure'

    def get_queryset(self):
        """Возвращает queryset по slug бани."""
        return Sauna.objects.filter(full_name=self.kwargs.get('slug'))


class ProjectDetailView(generic.DetailView):
    """
    Детальная страница проекта.
    """
    model = Project
    template_name = 'project-detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        """Возвращает queryset по slug проекта."""
        return Project.objects.filter(slug=self.kwargs.get('slug'))


class CategorySaunaView(generic.View):
    """
    Категории для бань.
    """
    template_name = 'categories.html'

    def get(self, request):
        categories = Category.objects.filter(saunas__isnull=False).distinct()

        context = {
            "categories": categories,
            "saunas_list": Sauna.objects.all(),
            "category_title": METATAGS.get('sauna', {}).get('title', ''),
            "category_description": METATAGS.get(
                'sauna', {}).get('description', ''),
        }

        return render(request, self.template_name, context)


class CategoryHousesView(generic.View):
    """
    Категории для домов.
    """
    template_name = "categories.html"

    def get(self, request):
        categories = Category.objects.filter(houses__isnull=False).distinct()

        context = {
            "categories": categories,
            "houses_list": House.objects.all(),
            "category_title": METATAGS.get('house', {}).get('title', ''),
            "category_description": METATAGS.get(
                'house', {}).get('description', '')
        }

        return render(request, self.template_name, context)


class SubcategoriesHousesView(generic.View):
    """
    Страница подкатегории домов.
    """
    template_name = "structure-index.html"
    category_template_name = "categories.html"

    def get(self, request, cat_slug, sub_slug=None):
        """Отображает список домов по категории и подкатегории."""
        category = Category.objects.get(slug=cat_slug)
        houses = House.objects.filter(category=category)

        if sub_slug:
            subcategory = Category.objects.get(slug=sub_slug)

            desc_data = {}
            if category.subcategories_description:
                desc_data = category.subcategories_description.get(
                    str(subcategory.id), {}
                )
            header = desc_data.get('header') or subcategory.header_house
            title = desc_data.get('title') or subcategory.title_house
            description = desc_data.get(
                'description') or subcategory.description_house

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
    """
    Страница подкатегории бань.
    """
    template_name = "structure-index.html"
    category_template_name = "categories.html"

    def get(self, request, cat_slug, sub_slug=None):
        """Отображает список бань по категории и подкатегории."""
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


def detail(request, structure_name):
    """
    Поддержка старых URL: ищет дом или баню по полному имени.
    """
    structure = House.objects.filter(
        full_name=structure_name
    ).first() or Sauna.objects.filter(full_name=structure_name).first()

    if not structure:
        return redirect('/not-found/')
    return render(request, 'structure-detail.html', {'structure': structure})

#TODO вероятно уже избыточна, т.к. есть хендлер на ошибки
