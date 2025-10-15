from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Prefetch, Case, When, Value, IntegerField

from .models import House, Sauna, Project, Category, HouseImage, SaunaImage, filter_by_all_categories
from .constants import CATEGORY_NA_SVAYAH_TEXT, CATEGORY_DOMA_BANI_TEXT


def order_categories(qs):
    """
    Числовые названия (^\d) идут первыми, затем по priority и name.
    """
    return (
        qs.annotate(
            _num_first=Case(
                When(name__regex=r'^\d', then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by('_num_first', 'priority', 'name')
        .distinct())


def get_menu_categories(related_name):
    """
    Возвращает кортеж (size_categories, floor_categories, selection_categories)
    для выпадающего меню. Единая точка получения категорий для меню.
    """
    categories = Category.objects.filter(
        **{f"{related_name}__isnull": False}
    ).filter(is_visible=True).distinct()

    categories = order_categories(categories)

    return (
        categories.filter(is_size=True),
        categories.filter(is_floor=True),
        categories.filter(is_selection=True),
    )


house_images_prefetch = Prefetch(
    'images',
    queryset=HouseImage.objects.order_by('order'),
    to_attr='prefetched_images',
)
house_cover_prefetch = Prefetch(
    'images',
    queryset=HouseImage.objects.filter(is_cover=True).order_by('order'),
    to_attr='cover_images',
)

sauna_images_prefetch = Prefetch(
    'images',
    queryset=SaunaImage.objects.order_by('order'),
    to_attr='prefetched_images',
)
sauna_cover_prefetch = Prefetch(
    'images',
    queryset=SaunaImage.objects.filter(is_cover=True).order_by('order'),
    to_attr='cover_images',
)


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
    # slug_field = 'full_name'
    # slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            House.objects
            .filter(pub_date__lte=timezone.now())
            .prefetch_related(house_images_prefetch, house_cover_prefetch))


class SaunaDetailView(generic.DetailView):
    """
    Детальная страница бани.
    """
    model = Sauna
    template_name = 'structure-detail.html'
    context_object_name = 'structure'
    # slug_field = 'full_name'
    # slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Sauna.objects
            .filter(pub_date__lte=timezone.now())
            .prefetch_related(sauna_images_prefetch, sauna_cover_prefetch))


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
        categories = categories.filter(is_visible=True)
        categories = order_categories(categories)

        size_categories, floor_categories, selection_categories = get_menu_categories(self.related_name)

        qs = self.object_model.objects.filter(pub_date__lte=timezone.now())
        if self.object_model is House:
            qs = qs.prefetch_related(
                house_images_prefetch, house_cover_prefetch).order_by('?')[:30]
        elif self.object_model is Sauna:
            qs = qs.prefetch_related(
                sauna_images_prefetch, sauna_cover_prefetch).order_by('?')[:30]
        context = {
            "categories": categories,
            self.list_context_key: qs,
            "category_title": settings.METATAGS.get(self.meta_key, {}).get('title', ''),
            "category_description": settings.METATAGS.get(self.meta_key, {}).get('description', ''),
            "size_categories": size_categories,
            "floor_categories": floor_categories,
            "selection_categories": selection_categories,
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

    def get_category_description(self, category_slug):
        """Возвращает специальный текст для конкретных категорий"""
        category_texts = {
            'na-svayah': CATEGORY_NA_SVAYAH_TEXT,
            'doma-bani': CATEGORY_DOMA_BANI_TEXT,
        }
        return category_texts.get(category_slug, '')

    def get(self, request, cat_slug, sub_slug=None):
        category = get_object_or_404(Category, slug=cat_slug)
        base_qs = self.model.objects.filter(pub_date__lte=timezone.now())
        if sub_slug:
            subcategory = get_object_or_404(
                Category,
                slug=sub_slug,
                parent=category,
            )
            objects = filter_by_all_categories(base_qs, category, subcategory)
            desc_data = category.subcategories_description.get(
                str(subcategory.id), {}
            ) if category.subcategories_description else {}

            header = desc_data.get('header') or getattr(
                subcategory, f'header_{self.category_field_prefix}'
            )
            title = desc_data.get('title') or getattr(
                subcategory, f'title_{self.category_field_prefix}'
            )
            description = desc_data.get('description') or getattr(
                subcategory, f'description_{self.category_field_prefix}'
            )

        else:
            objects = base_qs.filter(category=category).distinct()

            header = getattr(category, f'header_{self.category_field_prefix}')
            title = getattr(category, f'title_{self.category_field_prefix}')
            description = getattr(category, f'description_{self.category_field_prefix}')
        if self.model is House:
            objects = objects.prefetch_related(house_images_prefetch, house_cover_prefetch).order_by('?')[:30]
        elif self.model is Sauna:
            objects = objects.prefetch_related(sauna_images_prefetch, sauna_cover_prefetch).order_by('?')[:30]

        category_specific_text = self.get_category_description(cat_slug)
        base_url = 'houses-categories' if self.model is House else 'saunas-categories'

        context = {
            self.list_context_key: objects,
            "category_description": description,
            "category_specific_text": category_specific_text,
            "category_title": title,
            "category_header": header,
            "base_url": base_url,
        }
        subcategories = category.subcategory.all()
        subcategories = order_categories(subcategories)
        if subcategories:
            context.update({
                "categories": subcategories,
                "curr_category": category,
            })

        if sub_slug:
            context.update({
                "curr_category": category,
                "is_subcategory": True,
                "back_to_categories_url": f"/{base_url}/",
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
