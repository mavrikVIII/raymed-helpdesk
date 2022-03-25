from django import forms
from .models import Person, Device, Subdevice
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Форма добавления нового сотрудника
class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = ["user", "first_name", "last_name", "middle_name",'email','date_birthday', 'department', 'image']

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].help_text = 'Обязательное поле'
        self.fields['last_name'].help_text = 'Обязательное поле'

class EditPersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ["first_name", "last_name", "middle_name",'date_birthday', 'email','department', 'image']
        widgets = {
            'email': forms.TextInput(attrs={'size':'100%'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditPersonForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].help_text = 'Обязательное поле'
        self.fields['last_name'].help_text = 'Обязательное поле'


# Форма добавления нового устройства
class DeviceForm(ModelForm):
    class Meta:
        model = Device
        amount = forms.IntegerField()
        fields = ['person', 'device_type', "model", 'descriptions', 'serial_number', 'number_account', 'provider', 'organization','closed_document', 'cost' ]
        widgets = {
            'descriptions': Textarea(attrs={'rows': 3, 'cols': "100%"}),
        }

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['device_type'].help_text = 'Обязательное поле'
        self.fields['model'].help_text = 'Обязательное поле'
        self.fields['serial_number'].help_text = 'Обязательное поле'

# Форма для добавления конкретному сотруднику устройства на странице detail
class DeviceFormPerson(ModelForm):
    class Meta:
        model = Device
        fields = ['device_type', "model", 'descriptions', 'serial_number', 'number_account', 'provider', 'organization', 'closed_document', 'cost' ]
        widgets = {
            'descriptions': Textarea(attrs={'rows': 3, 'cols': "100%"}),
        }

    def __init__(self, *args, **kwargs):
        super(DeviceFormPerson, self).__init__(*args, **kwargs)
        self.fields['device_type'].help_text = 'Обязательное поле'
        self.fields['model'].help_text = 'Обязательное поле'
        self.fields['serial_number'].help_text = 'Обязательное поле'

# Форма для добавления подустройства определенному устройству
class SubdeviceForDeviceForm(ModelForm):
    class Meta:
        model = Subdevice
        fields = ['type', "model", 'descriptions', 'serial_number', 'number_account', 'provider', 'organization', 'closed_document', 'cost' ]
        widgets = {
            'descriptions': Textarea(attrs={'rows': 3, 'cols': "100%"}),
        }

    def __init__(self, *args, **kwargs):
        super(SubdeviceForDeviceForm, self).__init__(*args, **kwargs)
        self.fields['type'].help_text = 'Обязательное поле'
        self.fields['model'].help_text = 'Обязательное поле'
        self.fields['serial_number'].help_text = 'Обязательное поле'

#Форма добавления перемещения\редактирования подустройства
class SubdeviceForm(ModelForm):
    class Meta:
        model = Subdevice
        fields = ['device','type', "model", 'descriptions', 'serial_number', 'number_account', 'provider', 'organization', 'closed_document', 'cost' ]
        widgets = {
            'descriptions': Textarea(attrs={'rows': 3, 'cols': "100%"}),
        }

    def __init__(self, *args, **kwargs):
        super(SubdeviceForm, self).__init__(*args, **kwargs)
        self.fields['type'].help_text = 'Обязательное поле'
        self.fields['model'].help_text = 'Обязательное поле'
        self.fields['serial_number'].help_text = 'Обязательное поле'
