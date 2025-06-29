from django.urls import path

from .views import (
    CategorySaunaView,
    CategoryHousesView,
    SubcategoriesHousesView,
    SubcategoriesSaunasView
)
from . import views

app_name = 'houses'

urlpatterns = [
    path('projects/', views.IndexView.as_view(), name='index'),
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
    path(
        'projects/<slug:slug>/',
        views.ProjectDetailView.as_view(),
        name='project-detail'
    ),
    path(
        'houses/<slug:slug>/',
        views.HouseDetailView.as_view(),
        name='house-detail'
    ),
    path(
        'saunas/<slug:slug>/',
        views.SaunaDetailView.as_view(),
        name='sauna-detail'
    ),
]
