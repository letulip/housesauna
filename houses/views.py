from itertools import chain
import logging

from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.db import models
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import House, Sauna, Project, Category

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    """
    Страница, отображающая список всех проектов.
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
                self.get_object_list(Project)
            )
        )
        return result_list

    def get_context_data(self, **kwargs: dict) -> object:
        """Добавляет в контекст количество и список проектов."""
        context = super(IndexView, self).get_context_data(**kwargs)
        context['projects_count'] = self.get_object_count(Project)
        context['projects_list'] = self.get_object_list(Project)
        context['category_header'] = "Проекты домов и бань"
        return context


class HouseDetailView(generic.DetailView):
    """
    Детальная страница дома.
    """
    model = House
    template_name = 'structure-detail.html'
    context_object_name = 'structure'
    slug_field = 'full_name'
    slug_url_kwarg = 'slug'


class SaunaDetailView(generic.DetailView):
    """
    Детальная страница бани.
    """
    model = Sauna
    template_name = 'structure-detail.html'
    context_object_name = 'structure'
    slug_field = 'full_name'
    slug_url_kwarg = 'slug'


class ProjectDetailView(generic.DetailView):
    """
    Детальная страница проекта.
    """
    model = Project
    template_name = 'project-detail.html'
    context_object_name = 'project'
    slug_field = 'full_name'
    slug_url_kwarg = 'slug'


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
            "category_title": settings.METATAGS.get(
                'sauna', {}).get('title', ''),
            "category_description": settings.METATAGS.get(
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
            "category_title": settings.METATAGS.get(
                'house', {}).get('title', ''),
            "category_description": settings.METATAGS.get(
                'house', {}).get('description', '')
        }

        return render(request, self.template_name, context)


class BaseSubcategoryView(generic.View):
    """
    Базовая модель подкатегорий
    model = House или Sauna
    category_field_prefix = 'house' или 'sauna',
    list_context_key = 'houses_list' или 'saunas_list'
    """
    model = None
    category_field_prefix = ''
    list_context_key = ''

    template_name = "structure-index.html"
    category_template_name = "categories.html"

    def get(self, request, cat_slug, sub_slug=None):
        category = get_object_or_404(Category, slug=cat_slug)
        objects = self.model.objects.filter(category=category)

        if sub_slug:
            subcategory = get_object_or_404(Category, slug=sub_slug)
            objects = self.model.objects.filter(category=subcategory)

            desc_data = category.subcategories_description.get(
                str(subcategory.id), {}) if category.subcategories_description else {}
            header = desc_data.get('header') or getattr(
                subcategory, f'header_{self.category_field_prefix}')
            title = desc_data.get('title') or getattr(
                subcategory, f'title_{self.category_field_prefix}')
            description = desc_data.get('description') or getattr(
                subcategory, f'description_{self.category_field_prefix}')
        else:
            header = getattr(category, f'header_{self.category_field_prefix}')
            title = getattr(category, f'title_{self.category_field_prefix}')
            description = getattr(
                category, f'description_{self.category_field_prefix}')

        context = {
            self.list_context_key: objects,
            "category_description": description,
            "category_title": title,
            "category_header": header,
        }

        subcategories = category.subcategory.all()
        if subcategories:
            context.update({
                "categories": subcategories,
                "curr_category": category,
            })

        template = self.category_template_name if subcategories and not sub_slug else self.template_name
        return render(request, template, context)


class SubcategoriesHousesView(BaseSubcategoryView):
    """
    Страница подкатегории домов.
    """
    model = House
    category_field_prefix = 'house'
    list_context_key = 'houses_list'


class SubcategoriesSaunasView(BaseSubcategoryView):
    """
    Страница подкатегории бань.
    """
    model = Sauna
    category_field_prefix = 'sauna'
    list_context_key = 'saunas_list'
