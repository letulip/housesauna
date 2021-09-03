from django.urls import path

from . import views

urlpatterns = [
  # path('', views.index, name='index'),
  path('', views.IndexView.as_view(), name='index'),
  path('<str:structure_name>/', views.detail, name='detail')
  # path('<str:structure_name>/', views.DetailView.as_view(), name='detail')
]