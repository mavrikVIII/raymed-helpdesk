from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField

#проверка на длину серии паспорта
def validators_serial(value):
    if not value.isdigit():
        raise forms.ValidationError(_("Серия паспорта должна состоять только из цифр"))
    elif len(str(value)) != 4 :
        raise forms.ValidationError(_('Серия пасорта должна состоять из 4 цифр'))

#проверка на длину серии паспорта
def validators_number(value):
    if not value.isdigit():
        raise forms.ValidationError(_("Номер паспорта должен состоять только из цифр"))
    elif len(str(value)) != 6 :
        raise forms.ValidationError(_('Номер пасорта должен состоять из 6 цифр'))

#проверка внутреннего телефона на правильность ввода(должны быть только цифры)
def validators_number_phone(value):
    if not value.isdigit():
        raise forms.ValidationError(_("Номер телефона должен состоять только из цифр"))

def validators_FIO(value):
    if not value.isalpha():
        raise forms.ValidationError(_("Это поле должно содержать только алфавитные символы"))

class Person(models.Model):
    DEPARTMENT_CHOICE = (
        ('manage', "Управление"),
        ('sekretary', "Секретариат"),
        ('buhgaltery' , "Бухгалтерия"),
        ('ekonom' , " Эконом.отдел"),
        ('legal' , "Правовой"),
        ('registration' , "Регистрации и сертификации"),
        ('commercial', "Коммерческий"),
        ("hr", "Управление персоналом"),
        ("tender" , "Тендерный"),
        ("warehouse", "Склад"),
        ("transport", "Транспортный"),
        ("logistics", "Логистика"),
        ("purchases", "Закупки"),
        ("security" , "Безопасность"),
        ("ahch",  "АХЧ"),
        ("it", "IT"),
        ("production", "Производство")
        )

    user = models.OneToOneField(User, blank = True, default = '0', on_delete = models.CASCADE)
    first_name = models.CharField('Имя',  max_length = 15, validators = [validators_FIO])
    last_name = models.CharField('Фамилия',  max_length = 15, validators = [validators_FIO])
    middle_name = models.CharField('Отчество', blank = True,  max_length = 15, validators = [validators_FIO])
    department = models.CharField('Отдел',  blank = True,   max_length = 20, choices = DEPARTMENT_CHOICE)
    # amount_laptop = models.IntegerField(default=0)
    # amount_desktop = models.IntegerField(default=0)
    # amount_monitor = models.IntegerField(default=0)
    # amount_monoblock = models.IntegerField(default=0)
    # amount_ex_disk = models.IntegerField(default=0)
    # amount_flash = models.IntegerField(default=0)
    date_add_person = models.DateTimeField('Дата добавление сотрудника в БД')
    image = models.ImageField('Фото', upload_to = 'images/avatar/',  blank=True)
    # internal_number_phone = models.CharField('Внутренний номер телефона', max_length = 3, blank = True,  validators = [validators_number_phone])
    # number_phone = models.CharField('Номер телефона', max_length = 11, blank = True, validators = [validators_number_phone] )
    date_birthday = models.DateField('Дата рождения',  blank = False)
    email = models.EmailField('Почта', max_length = 50, blank = True)
    email_password = models.CharField('Пароль для входа в почту', max_length = 50, blank = True) #скрытое поле. Нужно для отправки сообщений на почту почты



    # Сохранение ФИО в нижнем регистре
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.middle_name = self.middle_name.lower()
        return super(Person, self).save(*args, **kwargs)

    def __str__(self):
        s = self.last_name  + ' ' +self.first_name
        return s

    def soon_birthday(self):
        now = datetime.now()
        birthday = datetime(now.year, self.date_birthday.month, self.date_birthday.day)
        birthday2 = datetime(now.year+1, self.date_birthday.month, self.date_birthday.day)
        days = (min(birthday, birthday2) - now).days
        if days < 0:
            days += 365
        if days <= 30:
            return True
        else:
            return False

    def display_fname(self):
        return self.first_name[:1].upper() + self.first_name[1:]

    def display_lname(self):
        return self.last_name[:1].upper() + self.last_name[1:]

    def display_mname(self):
        return self.middle_name[:1].upper() + self.middle_name[1:]



    def display_number_phone(self):
        num = self.number_phone
        num = str('(%s)-%s-%s-%s' % (num[:1], num[1:4], num[4:6], num[6:8]))
        return num

    class Meta:
        verbose_name='Сотрудник'
        verbose_name_plural='Сотрудники'



class Device(models.Model):
    DEVICE_CHOICE = (
("desktop","Стационарный компьютер"),
("laptop", "Ноутбук"),
("monoblock", "Моноблок"),
("monitor", "Монитор"),
("externaldisk", "Внешний жесткий диск"),
("flashdrive", "Флешка"),
("periphery", "Мышь\клавиатура"),
("case", "Сумка"),
('other','Другое'),
)

    TYPE_ORGANIZATION = (
("raymed_tg_pvt","Раймед ТГ ПВТ"),
("raymed_t", "Раймед-Т"),
("miocardium", "Миокардиум"),
)
    person = models.ForeignKey(Person, null = True, blank = True, on_delete = models.SET_NULL)
    device_type =  models.CharField('Тип устройства',max_length = 15, choices = DEVICE_CHOICE )
    model = models.CharField('Модель устройства',max_length = 50)
    descriptions = models.TextField('Описание', null = True, blank = True)
    serial_number = models.CharField('Серийный номер', max_length = 25)
    number_account = models.CharField('Номер счета',max_length = 50,  blank = True) # номер счета
    provider =  models.CharField('Поставщик', max_length = 15, null = True, blank = True)
    cost = models.IntegerField('Стоимость(руб)', null = True, blank = True, default = 0)
    closed_document = models.FileField('Закрывающий документ', upload_to = 'documents/', blank = True, validators = [FileExtensionValidator(['pdf', 'jpg', 'docx'])])
    organization = models.CharField("Организация", max_length = 20, blank = True, null = True, choices = TYPE_ORGANIZATION)

    def display_person(self):
        person = self.person
        person = str(person).split(' ')
        return person[0][:1].upper()+person[0][1:]+' '+person[1][:1].upper() + person[1][1:]

    def __str__(self):
        return  str(self.person)+' '+ self.device_type +' ' +  self.model +' '+ self.serial_number

    def display_number_account(self):
        number_account = self.number_account
        return number_account.upper()

    class Meta:
        verbose_name='Устройство'
        verbose_name_plural='Устройства'

class Subdevice(models.Model):
    TYPE_HARDWARE = (
("ssd","SSD"),
("ram", "Оперативная память"),
)

    TYPE_ORGANIZATION = (
("raymed_tg_pvt","Раймед ТГ ПВТ"),
("raymed_t", "Раймед-Т"),
("miocardium", "Миокардиум"),
)
    device = models.ForeignKey(Device, on_delete = models.CASCADE)
    type = models.CharField('Тип устройства', max_length = 20, choices = TYPE_HARDWARE)
    model = models.CharField('Модель устройства',max_length = 50)
    descriptions = models.TextField('Описание', null = True, blank = True)
    serial_number = models.CharField('Серийный номер', max_length = 25)
    number_account = models.CharField('Номер счета',max_length = 50,  blank = True) # номер счета
    provider =  models.CharField('Поставщик', max_length = 15, null = True, blank = True)
    cost = models.IntegerField('Стоимость(руб)', null = True, blank = True, default = 0)
    closed_document = models.FileField('Закрывающий документ', upload_to = 'documents/', blank = True, validators = [FileExtensionValidator(['pdf', 'jpg', 'docx'])])
    organization = models.CharField("Организация", max_length = 20, blank = True, null = True, choices = TYPE_ORGANIZATION, default = TYPE_ORGANIZATION[0])

    def display_person(self):
        person = self.device.person
        person = str(person).split(' ')
        return person[0][:1].upper()+person[0][1:]+' '+person[1][:1].upper() + person[1][1:]

    def display_number_account(self):
        number_account = self.number_account
        return number_account.upper()

    def __str__(self):
        return self.type +' '+  self.model

    class Meta:
        verbose_name='Комплектующие'
        verbose_name_plural='Комплектующие'

class HistoryMoveDevice(models.Model):
    device = models.ForeignKey(Device, null = True, blank = True, on_delete = models.CASCADE)
    old_person = models.ForeignKey(Person, null = True, blank = True, default = None, on_delete = models.CASCADE)
    current_person = models.ForeignKey(Person, null = True, blank = True,  on_delete = models.CASCADE, related_name = 'current')
    date_get_device = models.DateField('Дата получения устройства', default = datetime.now())
    date_receive_device = models.DateField('Дата конца владения устройством', blank = True, null = True)

    def __str__(self):
        return str(self.device) +" "+ str(self.date_get_device)+" "+ str(self.date_receive_device)

    class Meta:
        verbose_name='История перемещения'
        verbose_name_plural='Истории перемещения'
