from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Client, Product, Proforma
from .forms import ClientForm, ProductForm, ProformaForm
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from uuid import uuid4

@login_required
def index(request):
    context = {
        'greeting': _("Welcome to our Project!"),
        'current_date': timezone.now(),
        'redirect_to': request.path,
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


    context = {}
    context['products'] = products
    context['proforma'] = proforma
 
    if request.method == 'GET':
        product_form = ProductForm()
        proforma_form = ProformaForm(instance=proforma)
        context['product_form'] = product_form
        context['proforma_form'] = proforma_form
        return render(request, 'formApp/proforma_create.html', context)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        proforma_form = ProformaForm(request.POST, instance=proforma)

        if product_form.is_valid():
            obj = product_form.save(commit=False)
            obj.proforma = proforma
            obj.save()

            messages.success(request, 'Invoice Product Added succesfully')
            return redirect('create-built-proforma', slug=slug)
        else:
            context['product_form'] = product_form
            context['proforma_form'] = proforma_form
            messages.error(request, 'Problem processing your request')
            return render(request, 'formApp/proforma_create.html', context)

    return render(request, 'formApp/proforma_create.html', context)
