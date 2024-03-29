"""housesauna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework import routers

from api.views import RealtyApiView, StructuresApiView
from . import views

handler404 = views.handler404

router = routers.DefaultRouter()

urlpatterns = [
    path('saunaman/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('', include(router.urls)),
    path(
        'api/v1/structures/',
        StructuresApiView.as_view(),
        name='get_structures'
    ),
    path(
        'api/v1/realty/',
        RealtyApiView.as_view(),
        name='get_realty'
    ),
    path('not-found/', views.notfound, name='notfound'),
    path('about/', views.about, name='about'),
    path('design/', views.design, name='design'),
    path('policy/', views.policy, name='policy'),
    path('production/', views.production, name='production'),
    path(
        'projects/',
        include(('houses.urls', 'houses'), namespace='houses')
    ),
    path('submit/', views.submit_form, name='submit'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
