from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class IndexViewSiteMap(Sitemap):
    """
    Sitemap для главной страницы.
    """
    changefreq = 'weekly'
    priority = 0.9

    def get_protocol(self, request=None):
        return "https"

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)
