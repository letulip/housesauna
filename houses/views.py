from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import House, Sauna, Project, Category


class ProjectsView(generic.ListView):
    """
    Страница, отображающая список всех проектов.
    """
    template_name = 'structure-index.html'
    context_object_name = 'all_structures'

    def get_queryset(self):
        """Возвращает список опубликованных проектов."""
        return Project.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        """Добавляет в контекст количество и заголовок."""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['projects_count'] = queryset.count()
        context['projects_list'] = queryset
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


class BaseCategoryView(generic.View):
    """
    Базовая вьюха категорий для рендера categories.html
    related_name = 'saunas' или 'houses'
    object_model = Sauna или House,
    meta_key = 'sauna' или 'house'
    list_context_key = 'saunas_list' или 'houses_list'
    """
    template_name = 'categories.html'
    related_name = ''
    object_model = None
    meta_key = ''
    list_context_key = ''

    def get(self, request):
        categories = Category.objects.filter(
            **{f"{self.related_name}__isnull": False}
        ).distinct()
        object_list = self.object_model.objects.all()
        context = {
            "categories": categories,
            self.list_context_key: object_list,
            "category_title": settings.METATAGS.get(
                self.meta_key, {}).get('title', ''),
            "category_description": settings.METATAGS.get(
                self.meta_key, {}).get('description', ''),
        }

        return render(request, self.template_name, context)


class CategorySaunaView(BaseCategoryView):
    """
    Страница категории бань.
    """
    related_name = 'saunas'
    object_model = Sauna
    meta_key = 'sauna'
    list_context_key = 'saunas_list'


class CategoryHousesView(BaseCategoryView):
    """
    Страница категории домов.
    """
    related_name = 'houses'
    object_model = House
    meta_key = 'house'
    list_context_key = 'houses_list'


class BaseSubcategoryView(generic.View):
    """
    Базовая вьюха подкатегорий
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
