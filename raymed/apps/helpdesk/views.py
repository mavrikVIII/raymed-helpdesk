from raymedasset.models import Device, Person, Subdevice
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group
from .forms import *
from django.urls import reverse
from django.core.mail import send_mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
from django.conf import settings
import os

def it_is_admin(request):
    return request.user.groups.filter(name='admins').exists()

def it_is_hr(request):
    return request.user.groups.filter(name='Hr').exists()

def it_is_buh(request):
    return request.user.groups.filter(name='buh').exists()


# @login_required(login_url = '/')
# def post_error(request, device_id):
#     username = request.user
#     user = User.objects.get(username = username)
#     device = Device.objects.get(id = device_id)
#     # person_msg = Person.objects.get()
#     if request.method == 'POST':
#         form = ErrorForm(request.POST, request.FILES)
#         if form.is_valid():
#             add_message_error = form.cleaned_data['message_error']
#             add_image_error = form.cleaned_data['image_error']
#             a = Error(person = user, device = device, message_error = add_message_error,  time_post_message = datetime.datetime.now(), image_error = add_image_error)
#             a.save()
#
#             msg = MIMEMultipart()
#             message = "Сообщение об ошибке от пользователя: %s"%(a.message_error, )
#             # setup the parameters of the message
#
#             if a.person.person.email:
#                 password = str(a.person.person.email_password)
#                 msg['From'] = str(a.person.person.email)
#             else:
#                 password = "I_Am_Marjahichev_1234"
#                 msg['From'] = "alexander.marjahichev@raymed.ru"
#             # print('----')
#             # print(a.person.person.email)
#             # print(a.person.person.email_password)
#             recipients = ['alexander.marjahichev@raymed.ru', 'mavrikVIII@yandex.ru', 'nirmal.dev@raymed.ru']
#             msg['To'] = ','.join(recipients)
#             msg['Subject'] = "Заявка от %s на устройстве %s %s"%(a.person, a.device.device_type, a.device.model)
#             # add in the message body
#             msg.attach(MIMEText(message, 'plain'))
#             #create server
#             server = smtplib.SMTP('smtp.office365.com: 587')
#             server.starttls()
#             # Login Credentials for sending the mail
#             server.login(msg['From'], password)
#             # send the message via the server.
#             server.sendmail(msg['From'], recipients, msg.as_string())
#             server.quit()
#
#             return redirect('..')
#     else:
#         form = ErrorForm()
#     context = { 'device':device, 'device_id':device_id , 'form': form, 'user':user}
#     return render(request, 'helpdesk/post_error.html', context)

@login_required(login_url = '/')
def views_errors_for_this_user(request, user_id):
    username = request.user
    user = User.objects.get(username = username)
    user_error = Error.objects.filter(person = username).order_by('time_post_message')[::-1]
    context = {'user':user, 'user_error' : user_error, 'user_id': user_id}
    print(len(user_error))
    return render(request, 'helpdesk/views_errors_for_this_user.html', context)

@login_required(login_url = '/')
def view_all_errors(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    status_wait = Error.objects.filter(status = 'wait').order_by('time_post_message')[::-1]
    status_work = Error.objects.filter(status = 'in_work').order_by('time_post_message')[::-1]
    status_ready = Error.objects.filter(status = 'ready').order_by('time_post_message')[::-1]

    content = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr,'status_wait':status_wait, 'status_work':status_work, 'status_ready':status_ready}
    return render(request, 'helpdesk/view_all_errors.html', content)

@login_required(login_url = '/')
def edit_error(request, error_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    error = Error.objects.get(id = error_id)
    if request.method == 'POST':
        form = EditErrorForm(request.POST)
        if form.is_valid():
            # edit_person = form.cleaned_data['person']
            # edit_device = form.cleaned_data['device']
            edit_message_error= form.cleaned_data['message_error']
            edit_status = form.cleaned_data['status']
            edit_solutions = form.cleaned_data['solutions']

            # error.person = edit_person
            # error.device = edit_device
            error.message_error = edit_message_error
            error.status = edit_status
            error.solutions = edit_solutions
            error.save()
            return HttpResponseRedirect(reverse('helpdesk:view_all_errors'))
    else:
        form = EditErrorForm(instance = error)
    context = {'form':form, 'error':error, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'error_id':error_id}
    return render(request, 'helpdesk/edit_error.html', context)

@login_required(login_url = '/')
def index_for_buh(request, user_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    user_buh = Person.objects.get(id = user_id)
    print(user_buh)
    context = {'user_buh': user_buh,'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr}
    return render(request, 'helpdesk/index_for_buh.html', context)

@login_required(login_url = '/')
def detail_error(request, error_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    error = Error.objects.get(id = error_id)
    print(error)
    context = {"error": error, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr}
    return render(request, 'helpdesk/detail_error.html', context)

# добавление неисправности без устройства
# @login_required(login_url = '/')
# def post_other_error(request):
#     username = request.user
#     user = User.objects.get(username = username)
#
#     if request.method == 'POST':
#         form = OtherErrorForm(request.POST, request.FILES)
#         if form.is_valid():
#             add_message_error = form.cleaned_data['message_error']
#             add_image_error = form.cleaned_data['image_error']
#             a = Error(person = user, message_error = add_message_error,  time_post_message = datetime.datetime.now(), image_error = add_image_error)
#             a.save()
#
#             msg = MIMEMultipart()
#             message = "Сообщение об ошибке от пользователя: %s"%(a.message_error )
#
#
#             if a.person.person.email:
#                 password = str(a.person.person.email_password)
#                 msg['From'] = str(a.person.person.email)
#             else:
#                 password = "I_Am_Marjahichev_1234"
#                 msg['From'] = "alexander.marjahichev@raymed.ru"
#
#             recipients = ['alexander.marjahichev@raymed.ru', 'mavrikVIII@yandex.ru', 'nirmal.dev@raymed.ru' ]
#             msg['To'] = ','.join(recipients)
#             msg['Subject'] = "Заявка от %s"%(a.person)
#             # add in the message body
#             msg.attach(MIMEText(message, 'plain'))
#             #create server
#             server = smtplib.SMTP('smtp.office365.com: 587')
#             server.starttls()
#             # Login Credentials for sending the mail
#             server.login(msg['From'], password)
#             # send the message via the server.
#             server.sendmail(msg['From'], recipients, msg.as_string())
#             server.quit()
#             return redirect('..')
#     else:
#         form = OtherErrorForm()
#     context = {'form': form, 'user':user}
#     return render(request, 'helpdesk/post_other_error.html', context)

@login_required(login_url = '/')
def post_global_error(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    username = request.user
    user = User.objects.get(username = username)
    person = Person.objects.get(user = username)
    devices_this_person = Device.objects.filter(person = person)

    if request.method == 'POST':
        form = ErrorForm(request.POST, request.FILES)
        if form.is_valid():
            add_message_error = form.cleaned_data['message_error']
            add_image_error = form.cleaned_data['image_error']

            add_device = request.POST.get('show_device_this_person')
            # Если ошибка на устройстве, то считывается его id в add_device и по id ищется устройство и к УСТРОЙСТВУ прикрепляется ошибка
            if str(add_device).isdigit():
                this_device = Device.objects.get(id = add_device)
                a = Error(person = user, device = this_device, message_error = add_message_error,  time_post_message = datetime.datetime.now(), image_error = add_image_error)
                a.save()
            # Если же в add_device гаходится не число(id) а СТРОКА other_device, то ошибка не прикрепляется к УСТРОЙСТВУ.
            else:
                a = Error(person = user, message_error = add_message_error,  time_post_message = datetime.datetime.now(), image_error = add_image_error)
                a.save()

            msg = MIMEMultipart()
            message = "Сообщение об ошибке от пользователя: %s\n"%(a.message_error )

            password = str(a.person.person.email_password)
            msg['From'] = str(a.person.person.email)

            recipients = [ 'mavrikVIII@yandex.ru', 'alexander.marjahichev@raymed.ru', 'nirmal.dev@raymed.ru']
            msg['To'] = ','.join(recipients)
            if a.device:
                msg['Subject'] = "Заявка от %s на устройстве %s %s."%(a.person, a.device.device_type, a.device.model)
            else:
                msg['Subject'] = "Заявка от %s." %(a.person)

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            if a.image_error:
                # Получение пути файла
                filename = str(a.image_error)
                filename = filename.split('/')
                filename = "\\".join(filename)
                abs_path = settings.MEDIA_ROOT + '\\' +  filename
                # Добавление в письмо самой картинки
                part = MIMEApplication(open(abs_path, 'rb').read())
                part.add_header('Content-Disposition', 'attachment', filename='error.png')
                msg.attach(part)


            #create server
            server = smtplib.SMTP('smtp.office365.com: 587')
            # server = smtplib.SMTP('smtp.yandex.ru')
            server.starttls()
            # Login Credentials for sending the mail
            server.login(msg['From'], password)
            # send the message via the server.
            server.sendmail(msg['From'], recipients, msg.as_string())
            server.quit()

            return redirect('..')
    else:
        form = ErrorForm()

    context = { 'form': form, 'user':user, 'devices_this_person':devices_this_person}
    return render(request, 'helpdesk/post_global_error.html', context)


# редактирование неисправности без устройства
# @login_required(login_url = '/')
# def edit_other_error(request, error_id):
#     is_admin = it_is_admin(request)
#     is_buh = it_is_buh(request)
#     is_hr = it_is_hr(request)
#
#     error = Error.objects.get(id = error_id)
#     if request.method == 'POST':
#         form = EditOtherErrorForm(request.POST)
#         if form.is_valid():
#             # edit_person = form.cleaned_data['person']
#             # edit_device = form.cleaned_data['device']
#             edit_message_error= form.cleaned_data['message_error']
#             edit_status = form.cleaned_data['status']
#             edit_solutions = form.cleaned_data['solutions']
#
#             # error.person = edit_person
#             # error.device = edit_device
#             error.message_error = edit_message_error
#             error.status = edit_status
#             error.solutions = edit_solutions
#             error.save()
#             return redirect('..')
#     else:
#         form = EditOtherErrorForm(instance = error)
#     context = {'form':form, 'error':error, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'error_id':error_id}
#     return render(request, 'helpdesk/edit_other_error.html', context)
