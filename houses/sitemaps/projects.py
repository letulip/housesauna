from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import Project


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def get_protocol(self, request=None):
        return "https"

    def items(self):
        return Project.objects.all()

    def location(self, item):
        return reverse('houses:project-detail', args=[item.slug])
