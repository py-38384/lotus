from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from .models import User
from .decorator import unauthenticated_user
from django.contrib.auth.decorators import login_required

# {% provider_login_url 'google' %}

@unauthenticated_user
def loginView(request):

    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            userobj = User.objects.get(email=user.email)
            if userobj.first_name and userobj.last_name:
                username = userobj.first_name + " " + userobj.last_name
            else:
                username = userobj.username
            messages.success(request,'<strong>Log in successful</strong> Welcome back {0}'.format(username))
            return redirect('home')
        else:
            messages.error(request,'Email or password is incorrect!!')
            return render(request,'login.html',context)
    return render(request,'login.html',context)

def logoutView(request):
    logout(request)
    messages.success(request,'<strong>Log out successful</strong>')
    return redirect('home')

@unauthenticated_user
def registrationView(request):
    form = CreateUserForm()
    context = {'form':form}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        agreed = request.POST.get('agree')
        password = request.POST.get('password1')
        if(agreed == 'on'):
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                user = authenticate(request, email=email, password=password)
                login(request,user)
                messages.success(request,'<strong>Account created successfully</strong> Welcome to MyCART {0}'.format(user.first_name+' '+user.last_name))
                return redirect('home')

            else:
                context['form'] = form
                return render(request,'register.html',context)
        else:
            messages.success(request,'You need to agree on our Terms of Service and Privary Policy.')
            return render(request,'register.html',context)

    return render(request,'register.html',context)

