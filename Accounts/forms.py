from django import forms
from django.contrib.auth import authenticate

from Accounts.models import User


class LoginForm(forms.Form):
    email = forms.CharField(required=True)

    password = forms.CharField(required=True)

    def clean_password(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(username=email, password=password)
        if not user:
            self.add_error("email", "Неправильный логин или пароль")
            self.add_error("password", "Неправильный логин или пароль")
        self.cleaned_data['user'] = user
        return password


class RegistrationForm(forms.Form):
    email = forms.CharField(required=True)

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    fpassword = forms.CharField(required=True)
    spassword = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.get_or_none(email=email)
        if user:
            self.add_error("email", "Такой email уже используется")
        return email

    def clean_firstpassword(self):
        password = self.cleaned_data['firstpassword']
        if len(password) < 8:
            self.add_error("firstpassword", "Не менее 10 сиволов")
        if ';' in password:
            self.add_error("firstpassword", "Недопустимый символ в пароле")
        return password

    def clean_secondpasswods(self):
        firstpassword = self.cleaned_data['firstpassword']
        secondpassword = self.cleaned_data['secondpassword']
        if firstpassword != secondpassword:
            self.add_error("secondpassword", "Пароли не совпадают")
        return secondpassword