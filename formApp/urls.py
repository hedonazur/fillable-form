from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from . import views

urlpatterns = [
    path('', views.index, name='formPage'),
    path('clients/', views.clients, name='clients'),
    path("company/", views.companySettings, name='company'),
    path('products/', views.products, name='products'),
    path("proformas/", views.proformas, name='proformas'),
    path('i18n/', include('django.conf.urls.i18n')),
    #Create url paths 
    path("proformas/create", views.createProforma, name='create-proforma'),
    path("proformas/create-build/<slug:slug>", views.createBuildProforma, name='create-built-proforma'),
]