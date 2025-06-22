from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import Category


class SubCategoryHouseSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        slugs = []
        categories = Category.objects.prefetch_related('parent').filter(
            parent__isnull=False,
            houses__isnull=False,
            parent__houses__isnull=False
        ).distinct()

        for category in categories:
            for parent in category.parent.all():
                slugs.append((parent.slug, category.slug))

        return slugs

    def location(self, item):
        parent, category = item
        return reverse('houses:houses_sub_list', args=[parent, category])


class SubCategorySaunaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        slugs = []
        categories = Category.objects.prefetch_related('parent').filter(
            parent__isnull=False,
            saunas__isnull=False,
            parent__saunas__isnull=False
        ).distinct()

        for category in categories:
            for parent in category.parent.all():
                slugs.append((parent.slug, category.slug))
        return slugs

    def location(self, item):
        parent, category = item
        return reverse('houses:sauna_sub_list', args=[parent, category])
