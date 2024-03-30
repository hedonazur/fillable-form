from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from . import views

urlpatterns = [
    path('', views.index, name='formPage'),
    path('clients/', views.clients, name='clients'),
    path('i18n/', include('django.conf.urls.i18n')),
]