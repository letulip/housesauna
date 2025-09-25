from django.urls import path
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404, redirect

from .views import (
    CategorySaunaView,
    CategoryHousesView,
    SubcategoriesHousesView,
    SubcategoriesSaunasView
)
from . import views
from .models import House, Sauna

app_name = 'houses'

urlpatterns = [
    # path('projects/', views.ProjectsView.as_view(), name='index'),
    path('houses/', RedirectView.as_view(url='/houses-categories/', permanent=True)),
    path('saunas/', RedirectView.as_view(url='/saunas-categories/', permanent=True)),
    path(
        'saunas-categories/',
        CategorySaunaView.as_view(),
        name='sauna_categories'
    ),
    path(
        'houses-categories/',
        CategoryHousesView.as_view(),
        name='houses_categories'
    ),
    path(
        'houses-categories/<int:pk>/',
        views.HouseDetailView.as_view(),
        name='house-detail'
    ),
    path(
        'saunas-categories/<int:pk>/',
        views.SaunaDetailView.as_view(),
        name='sauna-detail'
    ),
    path(
        'saunas-categories/<slug:cat_slug>/',
        SubcategoriesSaunasView.as_view(),
        name='sauna_sub'
    ),
    path(
        'houses-categories/<slug:cat_slug>/',
        SubcategoriesHousesView.as_view(),
        name='houses_sub'
    ),
    path(
        'saunas-categories/<slug:cat_slug>/<slug:sub_slug>/',
        SubcategoriesSaunasView.as_view(),
        name='sauna_sub_list'
    ),
    path(
        'houses-categories/<slug:cat_slug>/<slug:sub_slug>/',
        SubcategoriesHousesView.as_view(),
        name='houses_sub_list'
    ),
    # path(
    #     'projects/<slug:slug>/',
    #     views.ProjectDetailView.as_view(),
    #     name='project-detail'
    # ),
]


def house_slug_redirect(request, slug):
    obj = get_object_or_404(House, full_name=slug)
    return redirect('houses:house_detail', pk=obj.pk, permanent=True)


def sauna_slug_redirect(request, slug):
    obj = get_object_or_404(Sauna, full_name=slug)
    return redirect('houses:sauna_detail', pk=obj.pk, permanent=True)


urlpatterns += [
    path('house/<slug:slug>/', house_slug_redirect, name='house_slug_redirect'),
    path('sauna/<slug:slug>/', sauna_slug_redirect, name='sauna_slug_redirect'),
]
