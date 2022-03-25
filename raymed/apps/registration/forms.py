from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    field_order = ['username', 'password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'

        # self.fields['email'].help_text = 'Введите ваш email'
        self.fields['password1'].help_text = '''
        <ul>
            <li>Ваш пароль не может сопадать с email </li>
            <li>Ваш пароль должен содержать как минимум 8 символов. </li>
            <li>Постарайтесь придумать уникальный пароль </li>
            <li>Ваш пароль не должен быть полностью цифровым </li>
        </ul> '''
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'
