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
    
    #Delete an proforma
    path('proformas/delete/<slug:slug>',views.deleteProforma, name='delete-proforma'),
    #View pdf
    path('proformas/view-pdf/<slug:slug>',views.viewPDFProforma, name='view-pdf-proforma'),
    path('proformas/view-document/<slug:slug>',views.viewDocumentProforma, name='view-document-proforma'),
    path('invoices/email-document/<slug:slug>',views.emailDocumentProforma, name='email-document-proforma'),

]