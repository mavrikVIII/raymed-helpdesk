from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from raymedasset.models import Device, Person
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import forms
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from datetime import datetime

def it_is_admin(request):
    return request.user.groups.filter(name='admins').exists()

def it_is_hr(request):
    return request.user.groups.filter(name='Hr').exists()

def it_is_buh(request):
    return request.user.groups.filter(name='buh').exists()

def listss(request):
    return request.user.groups.all()

def home(request):
    #Если пользователь уже авторизован, то перекидывать его сразу на страницу Index
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('registration:index'))

    #Если пользователь хочет авторизоваться
    elif request.method == "POST":
        username = 'Пользователь'
        visible = False

        username = request.POST['login']
        password = request.POST['password']

        if authenticate(username = username, password = password):
            user = authenticate(username = username, password = password)
            login(request,user)
            is_admin = it_is_admin(request)
            is_hr = it_is_hr(request)
            is_buh = it_is_buh(request)
            # print(is_admin, is_hr, is_buh)
        else:
            username = 'Пользователь'
            visible = True
            context = {'visible': visible,'username':username}
            return render(request, 'registration/home.html', context )

        is_list = listss(request)
        all_person_sort_birthday = Person.objects.all().order_by("date_birthday")
        all_person = Person.objects.all().order_by("date_add_person")[::-1][:10]
        device_without_person = Device.objects.filter(person=None)

        if is_admin or is_hr or is_buh:
            if is_buh:
                print('is_buh')
                user_name = request.user
                user_name = Person.objects.get(user = user_name)
                print(user_name)
                context = {'all_person':all_person, 'device_without_person': device_without_person, 'user_name' : user_name,  'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'is_list' : is_list,
                'all_person_sort_birthday': all_person_sort_birthday }
            else:
                print(is_admin, is_hr, is_buh)
                context = {'all_person':all_person, 'device_without_person': device_without_person, 'username' : username,  'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'is_list' : is_list,
                'all_person_sort_birthday': all_person_sort_birthday }
            return render(request, "registration/index.html", context)
        else:
            user_1 = request.user
            user_1 = Person.objects.get(user = user)
            print(user_1)
            # print(is_admin, is_hr, is_buh)
            context = {'all_person':all_person, 'device_without_person': device_without_person, 'username' : username,  'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'is_list' : is_list,
            'all_person_sort_birthday': all_person_sort_birthday , 'user':user, 'user_1':user_1}
            return render(request, "helpdesk/index.html", context)

        # Если пользователь только зашел на страницу home.html
    else:
        username = 'Пользователь'
        context = {'username': username}
        return render(request, 'registration/home.html', context)

@login_required(login_url = '/')
def index(request): # главная страница
    is_admin = it_is_admin(request)
    is_hr = it_is_hr(request)
    is_buh = it_is_buh(request)
    all_person = Person.objects.all().order_by("date_add_person")[::-1][:10]
    all_person_sort_birthday = Person.objects.all().order_by("date_birthday")

    if request.user.is_authenticated:
        username = request.user
        is_list = listss(request)
        device_without_person = Device.objects.filter(person=None)
        amount_monitor=0;    amount_laptop=0;    amount_desktop=0;    amount_monoblock=0; amount_ex_disk=0; amount_flash=0;
        context = {'all_person': all_person, 'device_without_person': device_without_person, 'username': username,  'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'is_list' : is_list,
        'all_person_sort_birthday':all_person_sort_birthday}

        if is_admin or is_hr or is_buh:
            if is_buh:
                user_name = request.user
                user_name = Person.objects.get(user = user_name)
                context = {'all_person': all_person, 'device_without_person': device_without_person, 'user_name': user_name,  'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'is_list' : is_list,
                'all_person_sort_birthday':all_person_sort_birthday}
            return render(request, 'registration/index.html', context)
        else:
            user_1 = request.user
            user_1 = Person.objects.get(user = user_1)
            # print(user_1)
            context = {'all_person': all_person, 'device_without_person': device_without_person, 'username': username,  'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'is_list' : is_list,
            'all_person_sort_birthday':all_person_sort_birthday, 'user_1':user_1}
            return render(request, 'helpdesk/index.html', context)
