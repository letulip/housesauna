from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import Category


class BaseSubCategorySitemap(Sitemap):
    """
    Базовый класс для sitemap подкатегорий домов и бань.
    """

    changefreq = "weekly"
    priority = 0.6
    model_name = ''
    url_name = ''

    def get_protocol(self, request=None):
        return "https"

    def get_queryset(self):
        return Category.objects.prefetch_related('parent').filter(
            parent__isnull=False
        ).distinct()

    def items(self):
        pairs = []
        categories = self.get_queryset().filter(
            **{f'{self.model_name}__isnull': False,
               f'parent__{self.model_name}__isnull': False}
            )

        for category in categories:
            for parent in category.parent.all():
                pairs.append((parent.slug, category.slug))
        return pairs

    def location(self, item):
        parent_slug, sub_slug = item
        return reverse(self.url_name, args=[parent_slug, sub_slug])


class SubCategoryHouseSitemap(BaseSubCategorySitemap):
    """
    Sitemap подкатегорий домов.
    """
    model_name = 'houses'
    url_name = 'houses:houses_sub_list'


class SubCategorySaunaSitemap(BaseSubCategorySitemap):
    """
    Sitemap подкатегорий бань.
    """
    model_name = 'saunas'
    url_name = 'houses:sauna_sub_list'
