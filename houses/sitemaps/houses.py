from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import House


class HouseSitemap(Sitemap):
    """
    Sitemap для детальных страниц построенных домов.
    """
    changefreq = "monthly"
    priority = 0.6

    def get_protocol(self, request=None):
        return "https"

    def items(self):
        return House.objects.all()

    def location(self, item):
        return reverse('houses:house-detail', args=[item.slug])
