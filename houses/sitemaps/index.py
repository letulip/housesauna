from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class IndexViewSiteMap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)
