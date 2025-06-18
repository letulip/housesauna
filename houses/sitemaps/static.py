from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSiteMap(Sitemap):
    """
    Sitemap для статических страниц и страниц категорий.
    """

    def items(self):
        return [
            {'name': 'about', 'changefreq': 'yearly', 'priority': 0.4},
            {'name': 'design', 'changefreq': 'monthly', 'priority': 0.6},
            {'name': 'policy', 'changefreq': 'yearly', 'priority': 0.3},
            {'name': 'production', 'changefreq': 'monthly', 'priority': 0.6},
            {'name': 'houses:index', 'changefreq': 'monthly', 'priority': 0.8},
            {'name': 'houses:sauna_categories', 'changefreq': 'monthly', 'priority': 0.7},
            {'name': 'houses:houses_categories', 'changefreq': 'monthly', 'priority': 0.7},
        ]

    def location(self, item):
        return reverse(item['name'])

    def changefreq(self, item):
        return item['changefreq']

    def priority(self, item):
        return item['priority']
