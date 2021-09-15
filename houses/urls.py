from django.urls import path

from . import views

urlpatterns = [
  # path('', views.index, name='index'),
  path('', views.IndexView.as_view(), name='index'),
  path('<str:structure_name>/', views.detail, name='detail'),
  path('houses/<slug:slug>/', views.HouseDetailView.as_view(), name='detail'),
  path('saunas/<slug:slug>/', views.SaunaDetailView.as_view(), name='detail')
]