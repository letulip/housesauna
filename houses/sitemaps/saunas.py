from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import Sauna


class SaunaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Sauna.objects.all()

    def location(self, item):
        return reverse('houses:sauna-detail', args=[item.slug])
