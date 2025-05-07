from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return [
            'about',
            'design',
            'policy',
            'production',
            'houses:index',
            'houses:sauna_categories',
            'houses:houses_categories'
        ]

    def location(self, item):
        return reverse(item)
