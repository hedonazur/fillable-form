from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _


@login_required
def index(request):
    context = {
        'greeting': _("Welcome to our Project!"),
        'current_date': timezone.now(),
        'redirect_to': request.path
    }
    return render(request, 'formApp/dashboard.html', context)
