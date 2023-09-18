from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Order, Customer


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'min': f"{datetime.today().strftime('%Y-%m-%d')}"}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'pizda', 'placeholder': 'Борис'}))
    last_name = forms.CharField(label='Фамилмя', widget=forms.TextInput(attrs={'placeholder': 'Немцов'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': '+7 (987) 654 32 10'}))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'placeholder': 'г. Москва, ул. Поддубная...'}))
    comment = forms.CharField(label='Комментарий к заказу',widget=forms.Textarea(attrs={'class': 'fs20','placeholder': 'Ваш комментарий...'}))
    products_information = forms.CharField(label='',widget=forms.Textarea(attrs={'class': 'full_invisible_absolute'}))

    def clean_date(self):
        order_date = self.cleaned_data['date']
        if order_date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return order_date
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment','products_information'
        )


class RegisterUserForm(UserCreationForm):
    CHOICES = [('Мужской', 'Мужской'),
               ('Женский', 'Женский')]
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'pochta@mail.ru'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'Борис'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'placeholder': 'Немцов'}))

    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': '+7 987 654 32 10'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', )


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Login'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '********'}))
    class Meta:
        fields = ('username', 'password')
