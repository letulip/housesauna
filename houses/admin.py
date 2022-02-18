from django.contrib import admin

# Register your models here.
from .models import House, Sauna, Project

admin.site.register(House)
admin.site.register(Sauna)
admin.site.register(Project)
