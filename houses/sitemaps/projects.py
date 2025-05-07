from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from houses.models import Project


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def location(self, item):
        return reverse('houses:project-detail', args=[item.slug])