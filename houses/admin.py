from django.contrib import admin

from .models import House, Sauna, Project, Category

admin.site.register(Project)


@admin.register(Sauna)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'get_categories']

    @admin.display()
    def get_categories(self, obj):
        return [category for category in obj.category.all()]


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'get_categories']

    @admin.display()
    def get_categories(self, obj):
        return [category for category in obj.category.all()]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['priority', 'name', 'slug', 'subcategory']
    prepopulated_fields = {'slug': ('name',)}
