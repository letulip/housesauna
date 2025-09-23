from collections import Counter

from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.db.models import Max

from .models import House, Sauna, Project, Category, HouseImage, SaunaImage


class ImageInlineFormSet(BaseInlineFormSet):
    """
    1) Не больше одной обложки.
    2) Уникальные order: 0,1,2... без дыр и дублей.
       Пустые/0/дубли — перенумеровываем.
    3) Если обложку не выбрали — назначаем её фото с минимальным order.
    """
    def clean(self):
        super().clean()
        db_max = (self.queryset.aggregate(m=Max('order'))['m']
                  if self.queryset is not None else None)
        next_free = -1 if db_max is None else int(db_max)

        cover_count = 0
        orders = []
        for form in self.forms:
            cd = getattr(form, 'cleaned_data', None)
            if not cd or cd.get('DELETE'):
                continue

            if cd.get('is_cover'):
                cover_count += 1

            order = cd.get('order')
            try:
                order = int(order)
            except (TypeError, ValueError):
                order = None
            orders.append(order)

        if cover_count > 1:
            raise ValidationError('Можно выбрать только одну обложку.')

        counts = Counter([o for o in orders if o is not None])
        kept_first_for = set()

        for form in self.forms:
            cd = getattr(form, 'cleaned_data', None)
            if not cd or cd.get('DELETE'):
                continue

            order = cd.get('order')
            try:
                order = int(order)
            except (TypeError, ValueError):
                order = None

            is_new = form.instance.pk is None
            is_empty = (order in (None, '', 0)) if is_new else (order in (None, ''))

            need_reassign = False
            if is_empty:
                need_reassign = True
            elif order is not None and counts.get(order, 0) > 1:
                if order in kept_first_for:
                    need_reassign = True
                else:
                    kept_first_for.add(order)

            if need_reassign:
                next_free += 1
                order = next_free

            form.instance.order = order
            cd['order'] = order
        if cover_count == 0:
            candidates = []
            for form in self.forms:
                cd = getattr(form, 'cleaned_data', None)
                if not cd or cd.get('DELETE'):
                    continue
                order = cd.get('order')

                has_image = bool(cd.get('image'))
                if not has_image and form.instance.pk:
                    has_image = bool(getattr(form.instance, 'image', None))

                if has_image:
                    candidates.append((order, form))

            if candidates:
                candidates.sort(key=lambda x: x[0])
                _, first_form = candidates[0]
                first_cd = first_form.cleaned_data
                first_form.instance.is_cover = True
                first_cd['is_cover'] = True

    def validate_unique(self):
        return


class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 1
    formset = ImageInlineFormSet
    fields = ('preview', 'image', 'order', 'is_cover',)
    readonly_fields = ('preview',)
    ordering = ('order',)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:80px;" />', obj.image.url)
        return "—"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj is not None:
            m = obj.images.aggregate(m=Max('order'))['m']
            next_order = 0 if m is None else m + 1
            formset.form.base_fields['order'].initial = next_order
        return formset


class SaunaImageInline(admin.TabularInline):
    model = SaunaImage
    extra = 1
    formset = ImageInlineFormSet
    fields = ('preview', 'image', 'order', 'is_cover',)
    readonly_fields = ('preview',)
    ordering = ('order',)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:80px;" />', obj.image.url)
        return "—"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj is not None:
            m = obj.images.aggregate(m=Max('order'))['m']
            next_order = 0 if m is None else m + 1
            formset.form.base_fields['order'].initial = next_order
        return formset


class BaseStructureAdmin(admin.ModelAdmin):
    """
    Единые настройки для Домов и Бань.
    """
    list_display = ['short_name', 'get_categories', 'title', 'square', 'price_per_m2', 'cost']
    readonly_fields = ['cost']

    @admin.display(description="Категории")
    def get_categories(self, obj):
        return ", ".join(map(str, obj.category.all()))

    def save_model(self, request, obj, form, change):
        """
        1) При первом сохранении можно назначить цену за м² по правилам,
           если она не выбрана.
        2) Пересчитать общую стоимость по формуле модели.
        """
        if not obj.price_per_m2:
            obj.assign_initial_price_per_m2()
        super().save_model(request, obj, form, change)
        obj.update_cost()

        selected = list(obj.category.all())
        parents = Category.objects.filter(subcategory__in=selected)
        to_add = [p for p in parents if p not in selected]
        if to_add:
            obj.category.add(*to_add)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'get_categories', 'title']

    @admin.display()
    def get_categories(self, obj):
        return [category for category in obj.category.all()]


@admin.register(House)
class HouseAdmin(BaseStructureAdmin):
    inlines = [HouseImageInline]


@admin.register(Sauna)
class SaunaAdmin(BaseStructureAdmin):
    inlines = [SaunaImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'priority',
        'name',
        'slug',
        'subcategory',
        'title_house',
        'description_house',
        'title_sauna',
        'description_sauna',
        'header_sauna',
        'header_house',
        'subcategories_description'
    ]
    prepopulated_fields = {'slug': ('name',)}
