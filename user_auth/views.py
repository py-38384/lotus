from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from validate_email import validate_email
from .forms import CreateUserForm
from django.conf import settings
from django.views import View
from .models import *
from .decorator import unauthenticated_user
from django.contrib.auth.decorators import login_required
from time import time
from random import randint
import random
import string
import sys
sys.path.append("..")
from .email.send_email import send_email
import os


# {% provider_login_url 'google' %}

 
def get_otp(size):
    all_chars = string.ascii_letters + string.digits
    otp = ""
    for i in range(size):
        otp += random.choice(all_chars)
    return otp

def send_otp(request):
    otp = get_otp(randint(10,25))
    email_body = 'this is your OTP to verify your email -> <b>{0}</b><br> Lotus team'.format(otp)
    email_result = send_email(
        sender_email=os.environ.get('PRIMARY_EMAIL'),
        receiver_email=request.user.email,
        sender_account_pass=os.environ.get('PRIMARY_EMAIL_PASSWORD'),
        mail_subject='Verify your email.',
        email_body=email_body
        )
    if email_result == True:
        otp_obj = Email_Verified.objects.get(user=request.user)
        otp_obj.last_otp = otp
        otp_obj.last_email_send = int(time())
        otp_obj.direct_email_send = False
        otp_obj.save()
        return {'otp':otp,'email_status':'Email successfully send','otp_obj':otp_obj}
    else:
        return {'otp':otp,'email_status':email_result,'otp_obj':{}}

def email_resend_justifications(request):
    otp_obj = Email_Verified.objects.get(user=request.user)
    time_waited = int(time())-int(otp_obj.last_email_send)
    if otp_obj.email_attempt_level == 1:
        time_wait_target = 60
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 2:
        time_wait_target = 120
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}

    elif otp_obj.email_attempt_level == 3:
        time_wait_target = 240
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 4:
        time_wait_target = 480
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 5:
        time_wait_target = 960
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 6:
        time_wait_target = 1920
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 7:
        time_wait_target = 3840
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 8:
        time_wait_target = 7680
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 9:
        time_wait_target = 15360
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    elif otp_obj.email_attempt_level == 10:
        time_wait_target = 46080
        if time_waited > time_wait_target:
            return {'email_resend_available':True,'first_time': False,'time_waited':time_waited,'time_wait_need':0}
        else:
            time_wait_need = time_wait_target - time_waited
            return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':time_wait_need}
    return {'email_resend_available':False,'first_time': False,'time_waited':time_waited,'time_wait_need':0}

def get_otp_input_wait_time(request):
    otp_obj = Email_Verified.objects.get(user=request.user)
    last_otp_input_time = otp_obj.last_otp_input_time
    otp_attempt_level = otp_obj.otp_attempt_level
    if otp_attempt_level == 1:
        wait_time_target = 60
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 2:
        wait_time_target = 120
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 3:
        wait_time_target = 240 
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 4:
        wait_time_target = 480 
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 5:
        wait_time_target = 960
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 6:
        wait_time_target = 1920
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 7:
        wait_time_target = 3840
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 8:
        wait_time_target = 7680
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 9:
        wait_time_target = 15360
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    if otp_attempt_level == 10:
        wait_time_target = 46080
        waited_time = int(time())-last_otp_input_time
        wait_time_need = wait_time_target - waited_time
        return {'wait_time_need':wait_time_need,'wait_time_target':wait_time_target,'waited_time':waited_time}
    
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
                if int(os.environ.get('ENAIL_VERIFICATION')):
                    is_valid = validate_email(email)
                    if is_valid:
                        user = authenticate(request, email=email, password=password)
                        login(request,user)
                        return redirect('conform_email')
                    messages.error(request,'Your email is not valid or does not Exist!')
                    return render(request,'register.html',context)
                user = authenticate(request, email=email, password=password)
                login(request,user)
                email_verified_obj = Email_Verified.objects.create(user=request.user)
                email_verified_obj.email_verified = True
                email_verified_obj.save()
                return redirect('home')
            else:
                context['form'] = form
                return render(request,'register.html',context)
        else:
            messages.error(request,'You need to agree on our Terms of Service and Privary Policy.')
            return render(request,'register.html',context)

    return render(request,'register.html',context)

class Conform_Email(View):
    def get(self, request):
        context = {}
        email_verified_obj, email_verified_obj_created = Email_Verified.objects.get_or_create(user=request.user)
        if email_verified_obj.email_verified:
            raise Http404()
        if email_verified_obj_created or email_verified_obj.direct_email_send:
            otp_data_obj = send_otp(request)
            otp_data_obj['otp_obj'].attempt_remain = 5
            otp_data_obj['otp_obj'].otp_attempt_level = 0
            if email_verified_obj_created:
                otp_data_obj['otp_obj'].email_attempt_level = 1
            if not email_verified_obj_created and not email_verified_obj.once_email_verified:
                otp_data_obj['otp_obj'].email_attempt_level += 1
            otp_data_obj['otp_obj'].save()
            email_resend_justifications_obj = email_resend_justifications(request)
            context['message'] = 'We emailed a OTP to <span class="bold">{0}</span>. Enter the OTP to conform your email.'.format(request.user.email)
            context['email_resend_time_wait_need'] = email_resend_justifications_obj['time_wait_need']
            return render(request, 'conform_email.html',context)
        if email_verified_obj.blocked:
                return redirect('block')
        email_resend_justifications_obj = email_resend_justifications(request)
        if email_verified_obj.otp_input_blocked:
            get_otp_input_wait_time_obj = get_otp_input_wait_time(request)
            if email_resend_justifications_obj['email_resend_available']:
                context['email_resend_available'] = True
            else:
                context['email_resend_time_wait_need'] = email_resend_justifications_obj['time_wait_need']
            if get_otp_input_wait_time_obj['waited_time'] > get_otp_input_wait_time_obj['wait_time_target']:
                email_verified_obj.otp_input_blocked = False
                email_verified_obj.save()
                context['message'] = 'We emailed a OTP to <span class="bold">{0}</span>. Enter the OTP to conform your email.'.format(request.user.email)
                return render(request,'conform_email.html',context)
            
            context['message'] = 'You need to wait to input your OTP'
            context['input_disable'] = True
            context['wait_time_need'] = get_otp_input_wait_time_obj['wait_time_need']
            return render(request, 'conform_email.html',context)
        
        context['message'] = 'We emailed a OTP to <span class="bold">{0}</span>. Enter the OTP to conform your email.'.format(request.user.email)
        if email_resend_justifications_obj['email_resend_available']:
            context['email_resend_available'] = True
        else:
            context['email_resend_time_wait_need'] = email_resend_justifications_obj['time_wait_need']
        return render(request,'conform_email.html',context)

    def post(self, request):
        if request.user.is_authenticated:
            context = {}
            user_otp = request.POST.get('otp')
            otp_obj = Email_Verified.objects.get(user=request.user)
            email_resend_justifications_obj = email_resend_justifications(request)
            if otp_obj.blocked:
                return redirect('block')
            if user_otp == None:
                get_otp_input_wait_time_obj = get_otp_input_wait_time(request)
                context['message'] = 'You need to wait in order to retry again.'
                context['email_resend_time_wait_need'] = email_resend_justifications_obj['time_wait_need']
                context['wait_time_need'] = get_otp_input_wait_time_obj['wait_time_need']
                return render(request, 'conform_email.html',context)
            if len(user_otp) == 0:
                context['message'] = 'Please enter a OTP..'
                return render(request, 'conform_email.html',context)
            if otp_obj.otp_input_blocked:
                get_otp_input_wait_time_obj = get_otp_input_wait_time(request)
                if get_otp_input_wait_time_obj['waited_time'] > get_otp_input_wait_time_obj['wait_time_target']:
                    otp_obj.otp_input_blocked = False
                    otp_obj.save()
                    if user_otp==otp_obj.last_otp:   
                        return self.otp_matched(request)
                    return self.otp_mismatched(request)
                context['message'] = 'You need to wait to input your OTP'
                context['input_disable'] = True
                context['wait_time_need'] = get_otp_input_wait_time_obj['wait_time_need']
                return render(request, 'conform_email.html',context)
            otp_obj.last_otp_input_time = int(time())
            otp_obj.save()
            if user_otp==otp_obj.last_otp:   
                return self.otp_matched(request)
            return self.otp_mismatched(request)
        else:
            raise Http404()
    def otp_matched(self,request):
        otp_obj = Email_Verified.objects.get(user=request.user)
        otp_obj.email_verified = True
        otp_obj.once_email_verified = True
        otp_obj.email_attempt_level = 1
        otp_obj.save()
        messages.success(request,'Your email ({0}) verification successfull.'.format(request.user.email))
        otp_obj.save()
        return redirect('home')
    def otp_mismatched(self,request):
        context = {}
        otp_obj = Email_Verified.objects.get(user=request.user)
        email_resend_justifications_obj = email_resend_justifications(request)
        if email_resend_justifications_obj['email_resend_available']:
                context['email_resend_available'] = True
        else:
            context['email_resend_time_wait_need'] = email_resend_justifications_obj['time_wait_need']
        if otp_obj.attempt_remain > 0:
            otp_obj.attempt_remain -= 1
            if otp_obj.attempt_remain == 0:
                otp_obj.otp_input_blocked = True
                if otp_obj.otp_attempt_level <= 10:
                    otp_obj.otp_attempt_level += 1
                    otp_obj.attempt_remain = 5
                    otp_obj.save()
                    get_otp_input_wait_time_obj = get_otp_input_wait_time(request)
                    context['message'] = 'You have used up all of your tries. relax for a moment.'
                    context['input_disable'] = True
                    context['wait_time_need'] = get_otp_input_wait_time_obj['wait_time_need']
                    return render(request, 'conform_email.html',context)
                otp_obj.blocked = True
                return redirect('block')
            otp_obj.save()
            context['message'] = 'Your given OTP does not matched. enter the correct one. <span class="bold">you have {0} tries</span>'.format(otp_obj.attempt_remain)
            context['attempt_remain'] = otp_obj.attempt_remain
            return render(request, 'conform_email.html',context)
    
def email_resend(request):
    if request.user.is_authenticated:
        email_resend_justifications_obj = email_resend_justifications(request)
        if email_resend_justifications_obj['email_resend_available'] == False and  otp_data_obj['otp_obj'].email_attempt_level > 10:
            otp_data_obj['otp_obj'].blocked = True
            otp_data_obj['otp_obj'].save()
            return redirect('block')
        if email_resend_justifications_obj['email_resend_available']:
            otp_data_obj = send_otp(request)
            otp_data_obj['otp_obj'].email_attempt_level += 1
            otp_data_obj['otp_obj'].attempt_remain = 5
            otp_data_obj['otp_obj'].otp_attempt_level = 0
            otp_data_obj['otp_obj'].otp_input_blocked = False
            otp_data_obj['otp_obj'].save()
            return redirect('conform_email')
        raise Http404()
    else:
        raise Http404()

def block(request):
    otp_obj = Email_Verified.objects.get(user=request.user)
    if otp_obj.email_verified or request.user.socialaccount_set.exists():
        raise Http404()
    return render(request,'block.html')
                
class Change_Email(View):
    def get(self,request):
        otp_obj = Email_Verified.objects.get(user=request.user)
        if otp_obj.email_verified or request.user.socialaccount_set.exists():
            raise Http404()
        context = {'email':request.user.email}
        return render(request,'change_email_unverified.html', context)
    def post(self,request):
        context = {}
        otp_obj = Email_Verified.objects.get(user=request.user)
        if otp_obj.email_verified or request.user.socialaccount_set.exists():
            raise Http404()
        new_email = request.POST.get('new_email')
        if len(new_email) == 0:
                messages.error(request,'Please enter a valid Email..') 
                return render(request,'change_email_unverified.html', context)
        if User.objects.filter(email=new_email).exists():
            context = {'email':new_email}
            messages.error(request,'This email is already exist!!')
            return render(request,"change_email_unverified.html",context)
        context = {'email':new_email}
        user = User.objects.get(id=request.user.id)
        is_valid = validate_email(new_email)
        if is_valid:
            user.email = new_email
            user.save()
            otp_obj = Email_Verified.objects.get(user=request.user)
            otp_obj.email_verified = False
            otp_obj.otp_input_blocked = False
            otp_obj.direct_email_send = True
            otp_obj.save()
            return redirect('conform_email')
        messages.error(request,'This email ({0}) is not valid or not exist!!'.format(new_email))
        return render(request,'change_email_unverified.html', context)