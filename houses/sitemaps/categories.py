from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import Category


class CategoryHouseSitemap(Sitemap):
    """
    Sitemap для категорий домов.
    """
    changefreq = "monthly"
    priority = 0.7

    def get_protocol(self, request=None):
        return "https"

    def items(self):
        return Category.objects.filter(houses__isnull=False).distinct()

    def location(self, item):
        return reverse('houses:houses_sub', args=[item.slug])


class CategorySaunaSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def get_protocol(self, request=None):
        return "https"

    def items(self):
        return Category.objects.filter(saunas__isnull=False).distinct()

    def location(self, item):
        return reverse('houses:sauna_sub', args=[item.slug])
