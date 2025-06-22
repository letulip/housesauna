from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import House


class HouseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return House.objects.all()

    def location(self, item):
        return reverse('houses:house-detail', args=[item.slug])
