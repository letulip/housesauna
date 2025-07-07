from django.contrib import admin

from .models import House, Sauna, Project, Category


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'get_categories', 'title']

    @admin.display()
    def get_categories(self, obj):
        return [category for category in obj.category.all()]


@admin.register(Sauna)
class SaunaAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'get_categories', 'title']

    @admin.display()
    def get_categories(self, obj):
        return [category for category in obj.category.all()]


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'get_categories', 'title']

    @admin.display()
    def get_categories(self, obj):
        return [category for category in obj.category.all()]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'priority',
        'name',
        'slug',
        'subcategory',
        'title_house',
        'description_house',
        'title_sauna',
        'description_sauna',
        'header_sauna',
        'header_house',
        'subcategories_description'
    ]
    prepopulated_fields = {'slug': ('name',)}
