from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from api.views import RealtyApiView, StructuresApiView
from houses.sitemaps import sitemaps
from . import views

handler404 = views.handler404

urlpatterns = [
    path('saunaman/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
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
    path('submit/', views.submit_form, name='submit'),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('', include(('houses.urls', 'houses'), namespace='houses')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
