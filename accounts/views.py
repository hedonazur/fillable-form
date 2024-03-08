from .forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# Change password with old password
def user_change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                # Update user session
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect('/accounts/password_change/done')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, '../templates/registration/password_change_form.html', {'form': fm})
    else:
        return HttpResponseRedirect('/accounts/login')