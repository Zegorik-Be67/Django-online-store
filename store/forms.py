from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Store, Review

class NewProduct(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['image', 'title', 'description', 'whose', 'price']

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label='Запомнить меня',
    )
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']