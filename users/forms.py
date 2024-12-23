from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Логин"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"})
    )

    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Придумайте логин"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Придумайте пароль"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
