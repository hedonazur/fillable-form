from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Client
from .forms import ClientForm
from django.contrib import messages



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
