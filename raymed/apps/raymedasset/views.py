from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Device, Subdevice, HistoryMoveDevice
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group
from .forms import *
from django.urls import reverse
from itertools import chain

def it_is_admin(request):
    return request.user.groups.filter(name='admins').exists()

def it_is_hr(request):
    return request.user.groups.filter(name='Hr').exists()

def it_is_buh(request):
    return request.user.groups.filter(name='buh').exists()

@login_required(login_url = '/')
def detail_person(request, person_id): # детальная информация о сотруднике
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    images = 'images/icon.jpg'
    try:
        a = Person.objects.get(id = person_id)
    except:
        raise Http404("Сотрудик не найден")
    amount_desktop = Device.objects.filter(person = a).filter(device_type ='desktop').count()
    amount_laptop = Device.objects.filter(person = a).filter(device_type ='laptop').count()
    amount_monitor = Device.objects.filter(person = a).filter(device_type ='monitor').count()
    amount_monoblock = Device.objects.filter(person = a).filter(device_type ='monoblock').count()
    amount_ex_disk = Device.objects.filter(person = a).filter(device_type ='externaldisk').count()
    amount_flash = Device.objects.filter(person = a).filter(device_type ='flashdrive').count()

    context = {'name_person': a, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr,'images':images, 'amount_desktop':amount_desktop,
    'amount_laptop':amount_laptop, 'amount_monitor':amount_monitor, 'amount_monoblock':amount_monoblock, 'amount_ex_disk':amount_ex_disk,
    'amount_flash':amount_flash}
    return render(request, 'raymedasset/detail_person.html', context)

@login_required(login_url = '/')
def search_for_name(request, arg=''): # кнопка поиска сотрудника
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    # Если ф-я вызывается в выпадающем списке на index, то ей нужен аргумент arg, чтоб искать его
    if arg:
        list_person_lname = Person.objects.filter(last_name__startswith = arg)
        list_person_fname = Person.objects.filter(first_name__startswith = arg)

        if not list_person_lname and not list_person_fname:
            # raise Http404("Вы ввели некорректные данные")
            list_person=[]
            return list_person
        else:
            list_person = list_person_lname | list_person_fname
            return list_person
    # Если работает обычный поиск с страници index у бухгалтерии и кадров
    else:
        search_name = request.POST['search_first_name'].lower()
        list_person_lname = Person.objects.filter(last_name__startswith = search_name)
        list_person_fname = Person.objects.filter(first_name__startswith = search_name)

    if not list_person_lname and not list_person_fname:
        # raise Http404("Вы ввели некорректные данные")
        list_person=[]
        return list_person
    else:
        list_person = list_person_lname | list_person_fname
        print(list_person)
    # context={'person_name': a , 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'search_first_name': search_first_name, 'search_last_name' : search_last_name}
    context = {'list_person':list_person, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr,}
    return render(request, 'raymedasset/search_for_name.html', context)

@login_required(login_url = '/')
def search_for_type_device(request, arg = ''):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    search_type_device = request.POST['search_type_device']
    a = Device.objects.filter(device_type = search_type_device)

    count_type_device = len(a)
    context = { "list_search_type_device" : a, 'search_type_device': search_type_device, 'count_type_device' : count_type_device, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr}
    return render(request, 'raymedasset/search_for_type_device.html', context)

@login_required(login_url = '/')
def add_person_page(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            add_user = form.cleaned_data['user']
            add_first_name = form.cleaned_data['first_name']
            add_last_name = form.cleaned_data['last_name']
            add_middle_name = form.cleaned_data['middle_name']
            add_department = form.cleaned_data['department']
            add_date_birthday = form.cleaned_data['date_birthday']
            add_email = form.cleaned_data['email']
            date_add_person = timezone.now()

            # если картинку добавили вручную
            if form.cleaned_data['image']:
                add_avatar = form.cleaned_data['image']
            else:
                # иначе загружается стандартная картинка
                add_avatar = 'images/avatar/default_avatar.jpg'

            a = Person(user = add_user, first_name = add_first_name, last_name = add_last_name, middle_name = add_middle_name, department = add_department,
            date_add_person = date_add_person, image = add_avatar, date_birthday = add_date_birthday, email = add_email)
            a.save()
            return redirect('..')
    else:
        form = PersonForm()
    context = {'form' : form, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr,}
    return render(request, 'raymedasset/add_person_page.html', context)

@login_required(login_url = '/')
def add_device_page(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    if request.method == "POST":
        form = DeviceForm(request.POST, request.FILES)
        if form.is_valid():

            add_person = form.cleaned_data['person']
            add_device_type = form.cleaned_data['device_type']
            add_model = form.cleaned_data['model']
            add_descriptions = form.cleaned_data['descriptions']
            add_serial_number = form.cleaned_data['serial_number']
            add_number_account = form.cleaned_data['number_account'].lower()
            add_provider = form.cleaned_data['provider']
            add_cost = form.cleaned_data['cost']
            add_documents = form.cleaned_data['closed_document']

            # Проверка и забирание закрывающего документа с других позиций в Устройствах
            # если закр док-т не был загружен
            if not add_documents:
                # ищем док-т в Устройствах с таким же номером счета
                list_num_acc = Device.objects.filter(number_account = add_number_account)
                # если находим то присваем его себе и выходим из цикла сразу
                for i in list_num_acc:
                    if i.closed_document:
                        add_documents = i.closed_document
                        break
            # Если же нет в Устройствах не нашли, то ищем в Подустройствах
            elif not add_documents:
            # Проверка и забирание закрывающего документа с других позиций в Подустройств
            # ищем док-т в Устройствах с таким же номером счета
                list_num_acc_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                # если находим то присваем его себе и выходим из цикла сразу
                for i in list_num_acc_subdevice:
                    if i.closed_document:
                        add_documents = i.closed_document
                        break
            else:
                # Если есть закр. док-т то проверяет у всех УСТРОЙСТВ с таким номером счета. Если в других позициях нет закр.док-та, то ему добавляем
                list_num_acc = Device.objects.filter(number_account = add_number_account)
                for i in list_num_acc:
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()
                # Если есть закр. док-т то проверяет у всех ПОДУСТРОЙСТВ с таким номером счета. Если нет закр.док-та, то ему добавляем
                list_num_acc_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                for i in list_num_acc_subdevice:
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()

            a = Device(person = add_person, device_type = add_device_type, model = add_model, descriptions = add_descriptions, serial_number = add_serial_number,
            number_account = add_number_account, provider = add_provider, cost = add_cost, closed_document = add_documents )
            a.save()

            deviceHistory = HistoryMoveDevice(device = a, current_person = add_person)
            deviceHistory.save()

            print(a.closed_document)
            b = a.person
            if b:
                context = { 'add_person' : add_person, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr}
                return HttpResponseRedirect(reverse('raymedasset:detail_person', args=(b.id,)))
            else:
                return redirect('..')
    else:
        form = DeviceForm()
    context = {'form' : form,  'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr,}
    return render(request, 'raymedasset/add_device_page.html', context)

@login_required(login_url = '/')
def search_for_number_account(request, arg = ''):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
# Если ф-я вызывается в выпадающем списке на index, то ей нужен аргумент arg, чтоб искать его и она вызывается в ф-ии Search
    if arg:
        search_account = arg
        result_device = Device.objects.filter(number_account__startswith = search_account)
        result_subdevice = Subdevice.objects.filter(number_account__startswith = search_account)
        return result_device, result_subdevice
    else:
    # Если работает обычный поиск с страници index у бухгалтерии и кадров
        number_account_search = request.POST['search_for_number_account'].lower()
        result_device = Device.objects.filter(number_account__startswith = number_account_search)
        result_subdevice = Subdevice.objects.filter(number_account__startswith = number_account_search)

        context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'number_account_search' : number_account_search, 'result_device':result_device,
        'result_subdevice':result_subdevice}
        return render(request, "raymedasset/search_for_number_account.html", context)

@login_required(login_url = '/')
def see_all_device(request):

    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    all_deviced = Device.objects.all().order_by('device_type')
    count_device = len(all_deviced)
    context = {'all_deviced': all_deviced, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'count_device' : count_device }

    return render(request, 'raymedasset/see_all_device.html', context)

@login_required(login_url = '/')
def see_device_without_person(request):

    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    all_deviced_without_person = Device.objects.filter(person = None).order_by('device_type')
    count_device = len(all_deviced_without_person)
    context = {'all_deviced_without_person': all_deviced_without_person, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'count_device' : count_device }

    return render(request, 'raymedasset/see_device_without_person.html', context)

#добавление устройства конкретному сотруднику через страницу Detail
@login_required(login_url = '/')
def add_device_page_this_person(request, person_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    user_set = Person.objects.get(id = person_id)

    if request.method == "POST":
        form = DeviceFormPerson(request.POST, request.FILES)
        if form.is_valid():
            add_device_type = form.cleaned_data['device_type']
            add_model = form.cleaned_data['model']
            add_descriptions = form.cleaned_data['descriptions']
            add_serial_number = form.cleaned_data['serial_number']
            add_number_account = form.cleaned_data['number_account'].lower()
            add_provider = form.cleaned_data['provider']
            add_cost = form.cleaned_data['cost']
            add_documents = form.cleaned_data[ 'closed_document']

            # Проверка и забирание закрывающего документа с других позиций в Устройствах
            # если закр док-т не был загружен
            if not add_documents:
                # ищем док-т в Устройствах с таким же номером счета
                list_num_acc = Device.objects.filter(number_account = add_number_account)
                for i in list_num_acc:
                    # если находим то присваем его себе и выходим из цикла сразу
                    if i.closed_document:
                        add_documents = i.closed_document
                        break
            # Если же нет в Устройствах не нашли, то ищем в Подустройствах
            elif not add_documents:
                # Проверка и забирание закрывающего документа с других позиций в Подустройств
                # ищем док-т в Устройствах с таким же номером счета
                list_num_acc_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                for i in list_num_acc_subdevice:
                    # если находим то присваем его себе и выходим из цикла сразу
                    if i.closed_document:
                        add_documents = i.closed_document
                        break
            else:
                # Если есть закр. док-т то проверяет у всех УСТРОЙСТВ с таким номером счета. Если нет закр.док-та, то ему добавляем
                list_num_acc = Device.objects.filter(number_account = add_number_account)
                for i in list_num_acc:
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()
                # Если есть закр. док-т то проверяет у всех ПОДУСТРОЙСТВ с таким номером счета. Если нет закр.док-та, то ему добавляем
                list_num_acc_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                for i in list_num_acc_subdevice:
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()

            a = Device(person = user_set, device_type = add_device_type, model = add_model, descriptions = add_descriptions, serial_number = add_serial_number,
            number_account = add_number_account, provider = add_provider, cost = add_cost, closed_document = add_documents  )
            a.save()

            deviceHistory = HistoryMoveDevice(device = a, current_person = user_set)
            deviceHistory.save()

            return HttpResponseRedirect(reverse('raymedasset:detail_person', args=(person_id,)))
    else:
        form = DeviceFormPerson()

    context = {"person": user_set, "form":form, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, "person_id" : person_id}
    return render(request, 'raymedasset/add_device_page.html' , context )

@login_required(login_url = '/')
def transfer_device(request,device_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    device = Device.objects.get(id = device_id)

    if request.method == "POST":
        form = DeviceForm(request.POST, request.FILES)
        if form.is_valid():
            add_number_account = form.cleaned_data['number_account'].lower()
            add_person = form.cleaned_data['person']
            add_device_type = form.cleaned_data['device_type']
            add_model = form.cleaned_data['model']
            add_descriptions = form.cleaned_data['descriptions']
            add_serial_number = form.cleaned_data['serial_number']
            add_provider = form.cleaned_data['provider']
            add_cost = form.cleaned_data['cost']
            add_organization = form.cleaned_data['organization']

            # Если документ загружен, то мы загружаем всем УСТРОЙСТВАХ с таким же счетом этот док-т где его нет
            if form.cleaned_data['closed_document']:
                add_documents = form.cleaned_data['closed_document']
                device.closed_document = add_documents
                # загрузим закр док-т для всех УСТРОЙСТВ с таким номером счета
                list_this_number_account = Device.objects.filter(number_account = add_number_account)
                # Если существуеют УСТРОЙСТВА с такими счетами
                if list_this_number_account:
                    for i in list_this_number_account:
                        # Если убрать нижнее условие, то документ будет изменятсья у всех в процессе редактирования
                        if not i.closed_document:
                            i.closed_document = add_documents
                            i.save()
                # загрузим закр док-т для всех ПОДУСТРОЙСТВ с таким номером счета
                list_this_number_account_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                # Если существуеют ПОДУСТРОЙСТВА с такими счетами
                if list_this_number_account_subdevice:
                    for i in list_this_number_account_subdevice:
                        # Если убрать нижнее условие, то документ будет изменятсья у всех в процессе редактирования
                        if not i.closed_document:
                            i.closed_document = add_documents
                            i.save()
        # Если не загружать док-т, а изменить/добавить номер счета когда в БД уже есть закрывающий документ для этого номера счета
            else:
                if add_number_account:
                    if not(form.cleaned_data['closed_document']):
                        # создадим список с элементами у которых такой же номер счета
                        list_this_number_account_device = Device.objects.filter(number_account = add_number_account)
                        list_this_number_account_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                        # если в таблице Deivce есть, то смотрим тут
                        if list_this_number_account_device:
                            for i in list_this_number_account_device:
                                # и если у них у хотябы одного есть закрывающий документ, то мы его возьмем и добавим
                                if i.closed_document:
                                    add_closed_document = i.closed_document
                                    device.closed_document = add_closed_document
                                    break
                            # если нет в таблице Device, то смотрим в Subdevice
                        elif not(device.closed_document):
                            for i in list_this_number_account_subdevice:
                                # и если у них у хотябы одного есть закрывающий документ, то мы его возьмем и добавим
                                if i.closed_document:
                                    add_closed_document = i.closed_document
                                    device.closed_document = add_closed_document
                                    break

            device.person = add_person
            device.device_type = add_device_type
            device.model = add_model
            device.descriptions = add_descriptions
            device.serial_number =  add_serial_number
            device.number_account = add_number_account
            device.cost = add_cost
            device.provider = add_provider
            device.organization = add_organization
            device.save()

            deviceHistoryOld = HistoryMoveDevice.objects.filter(device = device).order_by('date_get_device')[::-1][0]
            deviceHistoryOld.date_receive_device = timezone.now()

            deviceHistory = HistoryMoveDevice(device = device, old_person = deviceHistoryOld.current_person , current_person = add_person)
            s1 = str(deviceHistory.old_person).strip()
            s2 = str(deviceHistory.current_person).strip()

            if s1 != s2:
                deviceHistory.save()
                deviceHistoryOld.save()

            if add_person:
                b = add_person.id
                return HttpResponseRedirect(reverse('raymedasset:detail_person', args=(b,)))
            else:
                return redirect('..')
    else:
        form = DeviceForm(instance=device)
    context = {'device': device, 'device_id' : device_id, 'form': form, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr}

    return render(request, 'raymedasset/transfer_device.html', context)

@login_required(login_url = '/')
def history_move_this_device(request, device_id):
    history_device = HistoryMoveDevice.objects.filter(device = device_id)
    # full_device()
    context = {'history_device' : history_device, }
    return render(request, 'raymedasset/history_this_device.html', context)

def full_device():
    all_device = Device.objects.all()
    # print(all_device)
    for device in all_device:
        if device.person:
            history_device = HistoryMoveDevice(device = device, current_person = device.person)
            history_device.save()

    return all_device

@login_required(login_url = '/')
def delete_device(request, device_id):
    a = Device.objects.get(id = device_id)
    a.delete()
    if a.person:
        b = a.person
        return HttpResponseRedirect(reverse("raymedasset:detail_person", args=(b.id,)))
    else:
        return redirect('..')

@login_required(login_url = '/')
def delete_subdevice(request, subdevice_id):
    a = Subdevice.objects.get(id = subdevice_id)
    a.delete()
    if a.device.person:
        b = a.device.person
        return HttpResponseRedirect(reverse("raymedasset:detail_person", args=(b.id,)))
    else:
        return redirect('..')

@login_required(login_url = '/')
def see_all_person(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    all_person = Person.objects.all().order_by('last_name')
    count_person = len(all_person)
    context = {'all_person': all_person, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'count_person' : count_person}
    return render(request, 'raymedasset/see_all_person.html', context)

@login_required(login_url = '/')
def edit_person(request, person_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    a = Person.objects.get(id = person_id)

    if request.method == 'POST':
        form = EditPersonForm(request.POST, request.FILES)
        if form.is_valid():
            add_first_name = form.cleaned_data['first_name']
            add_last_name = form.cleaned_data['last_name']
            add_middle_name = form.cleaned_data['middle_name']
            add_department = form.cleaned_data['department']
            add_date_birthday = form.cleaned_data['date_birthday']
            date_add_person = timezone.now()
            add_email = form.cleaned_data['email']

            if form.cleaned_data['image']:
                add_avatar = form.cleaned_data['image']
                a.image = add_avatar

            a.first_name = add_first_name
            a.last_name = add_last_name
            a.middle_name = add_middle_name
            a.department = add_department
            a.date_birthday = add_date_birthday
            a.email = add_email
            a.save()
            return HttpResponseRedirect(reverse("raymedasset:detail_person", args=(a.id,)))

    else:
        form = EditPersonForm(instance=a)
    l = len(str(a))

    context = {'person' : a, 'person_id':person_id, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr , 'form' : form }
    return render(request, 'raymedasset/edit_person.html', context)

# Поиск с выпадающего списка
@login_required(login_url = '/')
def search(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    if request.POST['select_search'] == 'name':
        search_name = request.POST['search_input'].lower()
        list_search_person = search_for_name(request, search_name) #вызываю ф-ию  search_for_name
        context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'list_search_person' : list_search_person}
    elif request.POST['select_search'] == 'number_account':
        search_number_account = request.POST['search_input'].lower()
        result_device, result_subdevice = search_for_number_account(request, search_number_account)  #вызываю ф-ию  search_for_number_account
        context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'result_device' : result_device, 'result_subdevice':result_subdevice}
    elif request.POST['select_search'] == 'serial_number':
        search_serial_number = request.POST['search_input']
        list_device = Device.objects.filter(serial_number__startswith = search_serial_number)
        list_subdevice = Subdevice.objects.filter(serial_number__startswith = search_serial_number)
        context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'list_device' : list_device, 'list_subdevice' :list_subdevice}

    return render(request, 'raymedasset/search.html', context)

@login_required(login_url = '/')
def see_device_for_number_account(request, number_account):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    number_account_search = number_account
    result_device = Device.objects.filter(number_account__startswith = number_account_search)
    result_subdevice = Subdevice.objects.filter(number_account__startswith = number_account_search)

    context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr,  'number_account_search' : number_account_search, 'result_device':result_device, 'result_subdevice':result_subdevice}
    return render(request, "raymedasset/see_device_for_number_account.html", context)

@login_required(login_url = '/')
def search_for_department(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    search_department =request.POST['search_department']

    department_list = Person.objects.filter(department__startswith = search_department)
    context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'department_list': department_list, 'search_department' : search_department}
    return render(request, 'raymedasset/search_for_department.html', context)

@login_required(login_url = '/')
def see_all_this_department(request, name_department):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    list_department = Person.objects.filter(department = name_department)
    count_person_department = len(list_department)
    context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'list_department': list_department, "name_department": name_department, 'count_person_department': count_person_department}
    return render(request, 'raymedasset/see_all_this_department.html', context)

@login_required(login_url = '/')
def see_all_this_type_device(request, type_device):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    list_device = Device.objects.filter(device_type = type_device)
    count_device = len(list_device)
    context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, 'list_device': list_device, "count_device": count_device}
    return render(request, 'raymedasset/see_all_this_type_device.html', context)

@login_required(login_url = '/')
def add_subdevice(request, device_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    device_set = Device.objects.get(id = device_id)
    if request.method == 'POST':
        form = SubdeviceForDeviceForm(request.POST, request.FILES)
        if form.is_valid():
            add_type = form.cleaned_data['type']
            add_model = form.cleaned_data['model']
            add_descriptions = form.cleaned_data['descriptions']
            add_serial_number = form.cleaned_data['serial_number']
            add_number_account = form.cleaned_data['number_account'].lower()
            add_provider = form.cleaned_data['provider']
            add_cost = form.cleaned_data['cost']
            add_documents = form.cleaned_data[ 'closed_document']
#
            # Проверка и забирание закрывающего документа с других позиций в Устройствах
            # если закр док-т не был загружен
            if not add_documents:
                # ищем док-т в Устройствах с таким же номером счета
                list_num_acc = Device.objects.filter(number_account = add_number_account)
                for i in list_num_acc:
                    # если находим то присваем его себе и выходим из цикла сразу
                    if i.closed_document:
                        add_documents = i.closed_document
                        break
            # Если же нет в Устройствах не нашли, то ищем в Подустройствах
            elif not add_documents:
            # Проверка и забирание закрывающего документа с других позиций в Подустройств
            # ищем док-т в Устройствах с таким же номером счета
                list_num_acc_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                for i in list_num_acc_subdevice:
                    # если находим то присваем его себе и выходим из цикла сразу
                    if i.closed_document:
                        add_documents = i.closed_document
                        break
                # Если есть закр. док-т то проверяет у всех УСТРОЙСТВ с таким номером счета. Если нет закр.док-та, то ему добавляем
                list_num_acc = Device.objects.filter(number_account = add_number_account)
                for i in list_num_acc:
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()
                # Если есть закр. док-т то проверяет у всех ПОДУСТРОЙСТВ с таким номером счета. Если нет закр.док-та, то ему добавляем
                list_num_acc_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                for i in list_num_acc_subdevice:
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()

            a = Subdevice(device = device_set, type = add_type, model = add_model,descriptions = add_descriptions, serial_number = add_serial_number,
            number_account = add_number_account, provider = add_provider,cost = add_cost, closed_document = add_documents)
            a.save()

            if a.device.person:
                b = a.device.person
                return HttpResponseRedirect(reverse('raymedasset:detail_person', args=(b.id,)))
            else:
                return redirect('..')
    else:
        form = SubdeviceForDeviceForm()
    context = {"device": device_set, "form":form, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, "device_id" : device_id}
    return render(request, 'raymedasset/add_subdevice_this_device.html', context)

@login_required(login_url = '/')
def transfer_subdevice(request, subdevice_id):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)

    subdevice = Subdevice.objects.get(id = subdevice_id)
    if request.method == "POST":
        form = SubdeviceForm(request.POST, request.FILES)
        if form.is_valid():
            add_device = form.cleaned_data['device']
            add_type = form.cleaned_data['type']
            add_model = form.cleaned_data['model']
            add_descriptions = form.cleaned_data['descriptions']
            add_serial_number = form.cleaned_data['serial_number']
            add_number_account = form.cleaned_data['number_account'].lower()
            add_provider = form.cleaned_data['provider']
            add_cost = form.cleaned_data['cost']
            add_organization = form.cleaned_data['organization']

            if form.cleaned_data['closed_document']:
                add_documents = form.cleaned_data['closed_document']
                subdevice.closed_document = add_documents
                # загрузим закр док-т для всех ПОДУСТРОЙСТВ с таким номером счета
                list_this_number_account = Subdevice.objects.filter(number_account = add_number_account)
                for i in list_this_number_account:
                    # Если убрать нижнее условие, то документ будет изменятсья у всех в процессе редактирования
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()
                # загрузим закр док-т для всех УСТРОЙСТВ с таким номером счета
                list_this_number_account_device = Device.objects.filter(number_account = add_number_account)
                for i in list_this_number_account_device:
                    # Если убрать нижнее условие, то документ будет изменятсья у всех в процессе редактирования
                    if not i.closed_document:
                        i.closed_document = add_documents
                        i.save()
            # Если изменить/добавить номер счета когда в БД уже есть закрывающий документ для этого номера счета
            else:
                if add_number_account:
                    if not(form.cleaned_data['closed_document']):
                        # создадим список с элементами у которых такой же номер счета
                        list_this_number_account_device = Device.objects.filter(number_account = add_number_account)
                        list_this_number_account_subdevice = Subdevice.objects.filter(number_account = add_number_account)
                        # если в таблице Deivce есть, то смотрим тут
                        if list_this_number_account_device:
                            for i in list_this_number_account_device:
                                # и если у них у хотябы одного есть закрывающий документ, то мы его возьмем и добавим
                                if i.closed_document:
                                    add_closed_document = i.closed_document
                                    subdevice.closed_document = add_closed_document
                                    break
                            # если нет в таблице Device, то смотрим в Subdevice
                        elif not(subdevice.closed_document):
                            for i in list_this_number_account_subdevice:
                                # и если у них у хотябы одного есть закрывающий документ, то мы его возьмем и добавим
                                if i.closed_document:
                                    add_closed_document = i.closed_document
                                    subdevice.closed_document = add_closed_document
                                    break

            subdevice.device = add_device
            subdevice.type = add_type
            subdevice.model = add_model
            subdevice.descriptions = add_descriptions
            subdevice.serial_number =  add_serial_number
            subdevice.number_account = add_number_account
            subdevice.cost = add_cost
            subdevice.provider = add_provider
            subdevice.organization = add_organization
            subdevice.save()

            if subdevice.device.person:
                b = subdevice.device.person
                return HttpResponseRedirect(reverse('raymedasset:detail_person', args=(b.id,)))
            else:
                return redirect('..')
    else:
        form = SubdeviceForm(instance = subdevice)
    context = {'subdevice': subdevice, "subdevice_id":subdevice_id, 'form': form, 'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr}

    return render(request, 'raymedasset/transfer_subdevice.html', context)

@login_required(login_url = '/')
def see_all_subdevice(request):
    is_admin = it_is_admin(request)
    is_buh = it_is_buh(request)
    is_hr = it_is_hr(request)
    all_subdevice = Subdevice.objects.all().order_by('type')
    count_subdevice = len(all_subdevice)
    context = {'is_admin' : is_admin, 'is_buh' : is_buh, 'is_hr' : is_hr, "all_subdevice":all_subdevice , 'count_subdevice' : count_subdevice}
    return render(request, 'raymedasset/see_all_subdevice.html', context)

@login_required(login_url = '/')
def test(request):
    devices = Device.objects.all()
    subdevices = Subdevice.objects.all()

    context = {'devices' : devices, 'subdevices' : subdevices}
    return render(request, 'raymedasset/test.html', context)
