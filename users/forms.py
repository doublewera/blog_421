from django import forms
from django.contrib.auth.forms import AuthenticationForm
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
