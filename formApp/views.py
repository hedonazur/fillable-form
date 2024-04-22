from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Client, Product, Proforma, Settings
from .forms import ClientForm, ProductForm, ProformaForm, ClientSelectForm
from .functions import emailProformaClient
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from uuid import uuid4

from django.http import HttpResponse
import pdfkit
from django.template.loader import get_template
from django.conf import settings
import os
import logging

logging.basicConfig(level=logging.DEBUG, filename="py_log.log", format="%(asctime)s %(levelname)s %(message)s")


@login_required
def index(request):
    context = {
    }
    return render(request, 'formApp/dashboard.html', context)


@login_required
def clients(request):
    context = {}
    clients = Client.objects.all()
    context['clients'] = clients

    if request.method == 'GET':
        form = ClientForm()
        context['form'] = form
        return render(request, 'formApp/clients.html', context)

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, 'New Client Added')
            return redirect('clients')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('clients')

    return render(request, 'formApp/clients.html', context)


@login_required
def products(request):
    context = {}
    products = Product.objects.all()
    context['products'] = products

    return render(request, 'formApp/products.html', context)


@login_required
def proformas(request):
    context = {}
    proformas = Proforma.objects.all()
    context['proformas'] = proformas

    return render(request, "formApp/proformas.html", context)

#####Create Proformas#######
@login_required
def createProforma(request):
    ####Create blank proforma
    number = "PROF-" + str(uuid4()).split('-')[1]
    newProforma = Proforma.objects.create(number=number)
    newProforma.save()

    proforma = Proforma.objects.get(number=number)
    return redirect('create-built-proforma', slug=proforma.slug)


@login_required
def createBuildProforma(request, slug):
    ###Fetch  proforma
    try:
        proforma = Proforma.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('proformas')
    
    ####Fetch product
    products = Product.objects.filter(proforma=proforma)
    items = 0
    if len(products) > 0:
        for x in products:
            y = int(x.quantity)
            items += y
    logging.info(f"The length of products: {len(products)}, number of items: {items} ")

    ####Update totals
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency

    proforma.total = invoiceTotal
    proforma.grandTotal = invoiceTotal + proforma.deliveryPrice

    context = {}
    context['products'] = products
    context['proforma'] = proforma
    context['items'] = items
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency
 
    if request.method == 'GET':
        product_form = ProductForm()
        proforma_form = ProformaForm(instance=proforma)
        client_form = ClientSelectForm(initial_client=proforma.client)
        context['product_form'] = product_form
        context['proforma_form'] = proforma_form
        context['client_form'] = client_form
        return render(request, 'formApp/proforma_create.html', context)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        proforma_form = ProformaForm(request.POST, instance=proforma)
        client_form = ClientSelectForm(request.POST, initial_client=proforma.client, instance=proforma)

        if product_form.is_valid():
            obj = product_form.save(commit=False)
            obj.proforma = proforma
            obj.save()

            messages.success(request, 'Proforma Product Added succesfully')
            return redirect('create-built-proforma', slug=slug)
        elif proforma_form.is_valid and 'salesmanName' in request.POST:
            proforma_form.save()

            messages.success(request, 'Proforma Updated succesfully')
            return redirect('create-built-proforma', slug=slug)
        elif client_form.is_valid and 'client' in request.POST:
            client_form.save()

            messages.success(request, 'Client added to Proforma succesfully')
            return redirect('create-built-proforma', slug=slug)
        else:
            context['product_form'] = product_form
            context['proforma_form'] = proforma_form
            context['client_form'] = client_form
            messages.error(request, 'Problem processing your request')
            return render(request, 'formApp/proforma_create.html', context)

    return render(request, 'formApp/proforma_create.html', context)


def companySettings(request):
    company = Settings.objects.get(clientFirstName='Office Solutions') 
    context = {'company': company}
    return render(request, 'formApp/company.html', context)


def viewPDFProforma(request, slug):
    ###Fetch  proforma
    try:
        proforma = Proforma.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('proformas')
    
    ####Fetch product
    products = Product.objects.filter(proforma=proforma)
    
    ####Get client Settings
    company = Settings.objects.get(clientFirstName='Office Solutions')

    #Calculate the proforma Total
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency

    context = {}
    context['products'] = products
    context['proforma'] = proforma
    context['company'] = company
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency

    return render(request, 'formApp/proforma_view.html', context)


def viewDocumentProforma(request, slug):
    ###Fetch  proforma
    try:
        proforma = Proforma.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('proformas')
    
    ####Fetch product
    products = Product.objects.filter(proforma=proforma)
    
    ####Get client Settings
    company = Settings.objects.get(clientFirstName='Office Solutions')

    #Calculate the proforma Total
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency

    context = {}
    context['products'] = products
    context['proforma'] = proforma
    context['company'] = company
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency

    #The name of your PDF file
    filename = '{}.pdf'.format(proforma.uniqueId)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('formApp/proforma_pdf_template.html')

    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
            'encoding': 'UTF-8',
            'javascript-delay':'10', #Optional
            'enable-local-file-access': None, #To be able to access CSS
            'page-size': 'A4',
            'custom-header' : [
                ('Accept-Encoding', 'gzip')
            ],
        }
        #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    #IF you have CSS to add to template
    css1 = os.path.join(settings.STATIC_ROOT, 'css/assets/dist/css', 'bootstrap.min.css')
    css2 = os.path.join(settings.STATIC_ROOT, 'css/assets/dist/css', 'bootstrap.min.css.map')
    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response


def emailDocumentProforma(request, slug):
    ###Fetch  proforma
    try:
        proforma = Proforma.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('proformas')
    
    ####Fetch product
    products = Product.objects.filter(proforma=proforma)
    
    ####Get client Settings
    company = Settings.objects.get(clientFirstName='Office Solutions')

    #Calculate the proforma Total
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency

    context = {}
    context['products'] = products
    context['proforma'] = proforma
    context['company'] = company
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency

    #The name of your PDF file
    filename = '{}.pdf'.format(proforma.uniqueId)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('formApp/proforma_pdf_template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'10', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    #Saving the File
    filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
    os.makedirs(filepath, exist_ok=True)
    pdf_save_path = filepath+filename
    #Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)


    #send the emails to client
    to_email = proforma.client.emailAddress
    from_client = company.clientFirstName
    emailProformaClient(to_email, from_client, pdf_save_path)

    proforma.status = 'EMAIL_SENT'
    proforma.save()

    #Email was send, redirect back to view - invoice
    messages.success(request, "Email sent to the client succesfully")
    return redirect('create-built-proforma', slug=slug)