from django.contrib import admin

# Register your models here.
from .models import House, Sauna

admin.site.register(House)
admin.site.register(Sauna)