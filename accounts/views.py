from .forms import UserCreationForm, PasswordChangeForm, UserLoginForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect


#Anonymous required
def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = 'home'

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator


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
    

@anonymous_required
def login(request):
    context = {}
    if request.method == 'GET':
        form = UserLoginForm()
        context['form'] = form
        return render(request, '../templates/registration/login.html', context)

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

            return redirect('home')
        else:
            context['form'] = form
            messages.error(request, 'Invalid Credentials')
            return redirect('login')


    return render(request, '../templates/registration/login.html', context)