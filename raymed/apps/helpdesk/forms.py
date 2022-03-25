from django import forms
from .models import Person, Device, Subdevice, Error
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Форма сообщения об ошибке
class ErrorForm(ModelForm):
    class Meta:
        model = Error
        fields = ["message_error", 'image_error']
        widgets = {
            'message_error': Textarea(attrs={'rows': 5, 'cols': "150%"}),
        }

    def __init__(self, *args, **kwargs):
        super(ErrorForm, self).__init__(*args, **kwargs)
        self.fields['message_error'].help_text = 'Обязательное поле'
        self.fields['image_error'].help_text = 'НЕ обязательное поле'

# форма редактирования неисправности
class EditErrorForm(ModelForm):
    class Meta:
        model = Error
        fields = ["message_error", 'status', 'solutions']
        widgets = {
            'message_error': Textarea(attrs={'rows': 5, 'cols': "150%"}),
            'solutions': Textarea(attrs={'rows': 5, 'cols': "150%"}),
        }

    def __init__(self, *args, **kwargs):
        super(EditErrorForm, self).__init__(*args, **kwargs)
        self.fields['message_error'].help_text = 'Обязательное поле'

# оишбка без техники, которая есть в БД
class OtherErrorForm(ModelForm):
    class Meta:
        model = Error
        fields = ["message_error", 'image_error']
        widgets = {
            'message_error': Textarea(attrs={'rows': 5, 'cols': "150%"}),
            'solutions': Textarea(attrs={'rows': 5, 'cols': "150%"}),
        }

    def __init__(self, *args, **kwargs):
        super(OtherErrorForm, self).__init__(*args, **kwargs)
        self.fields['message_error'].help_text = 'Обязательное поле'
        self.fields['image_error'].help_text = 'НЕ обязательное поле'


# форма редактирования неисправности без устройства
class EditOtherErrorForm(ModelForm):
    class Meta:
        model = Error
        fields = ["message_error", 'status', 'solutions']
        widgets = {
            'message_error': Textarea(attrs={'rows': 5, 'cols': "150%"}),
            'solutions': Textarea(attrs={'rows': 5, 'cols': "150%"}),
        }

    def __init__(self, *args, **kwargs):
        super(EditOtherErrorForm, self).__init__(*args, **kwargs)
        self.fields['message_error'].help_text = 'Обязательное поле'
