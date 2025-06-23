from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import Sauna


class SaunaSitemap(Sitemap):
    """
    Sitemap для карточек построенных бань.
    """
    changefreq = "monthly"
    priority = 0.6

    def get_protocol(self, request=None):
        return "https"

    def items(self):
        return Sauna.objects.all()

    def location(self, item):
        return reverse('houses:sauna-detail', args=[item.slug])
