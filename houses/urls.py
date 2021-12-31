from django.urls import path

from . import views

app_name = 'houses'

urlpatterns = [
  # path('', views.index, name='index'),
  path('', views.IndexView.as_view(), name='index'),
  path('<str:structure_name>/', views.detail, name='detail'),
  path('houses/<slug:slug>/', views.HouseDetailView.as_view(), name='house-detail'),
  path('saunas/<slug:slug>/', views.SaunaDetailView.as_view(), name='sauna-detail'),
  # path('sumbit/', views.SubmitFormHandler.as_view(), name='submit'),
]