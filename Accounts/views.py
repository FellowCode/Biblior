import urllib

from django.contrib.auth.decorators import login_required
from django.core import signing
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from django.contrib import auth
from django.conf import settings
from django.db.models import Q
import re
from urllib.parse import unquote
import json
from datetime import timedelta
from mail.smtp import SendRestoreMail

def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                auth.login(request, form.cleaned_data['user'])
                if request.GET.get('next'):
                    return redirect(request.GET['next'])
                return redirect(reverse('main:index'))
            for error in form['email'].errors:
                print(error)
            return render(request, 'Accounts/Login.html', {'form': form})
        form = LoginForm()
        return render(request, 'Accounts/Login.html', {'form': form})
    return redirect(reverse('main:index'))


def admin_login(request):
    p = urllib.parse.urlencode(request.GET)
    return redirect(f'{settings.LOGIN_URL}?' + p)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(email=form.cleaned_data['email'],
                                            password=form.cleaned_data['fpassword'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])
            auth.login(request, user)
            return redirect(reverse('main:index'))
        return render(request, 'Accounts/Registration.html', {'form': form})
    form = RegistrationForm()
    return render(request, 'Accounts/Registration.html', {'form': form})


@login_required
def personal_area(request):
    query = request.GET.get('query')
    if request.COOKIES.get('selected_cites'):
        sel_cites = list(map(int, json.loads(unquote(request.COOKIES.get('selected_cites')))))
    else:
        sel_cites = None

    if query:
        query = re.sub(' +', ' ', query)
        words = query.split(' ')
        pubs = None
        for word in words:
            qs = request.user.pubs.filter(Q(title__icontains=word) | Q(container_title__icontains=word)
                                          | Q(author__icontains=word) | Q(issued__icontains=word) |
                                          Q(issue__icontains=word) | Q(volume__icontains=word)).all()
            if not pubs:
                pubs = qs
            else:
                pubs.union(qs)
    else:
        pubs = request.user.pubs.all()
    return render(request, 'Accounts/PersonalArea.html', {'pubs': pubs, 'query': query, 'sel_cites': sel_cites})


@login_required
def change_password(request):
    if not request.method == 'POST':
        form = ChangePasswordForm(user=request.user)
        return render(request, 'Accounts/ChangePassword.html', {'form': form})
    # POST
    form = ChangePasswordForm(request.POST, user=request.user)
    if form.is_valid():
        request.user.set_password(form.cleaned_data['spassword'])
        request.user.save()
        auth.login(request, request.user)
        return redirect(reverse('accounts:personal_area'))
    return render(request, 'Accounts/ChangePassword.html', {'form': form})


def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.cleaned_data['user']
            SendRestoreMail(user)
            return render(request, 'Accounts/RestoreEmailSend.html', {'email': email})
        return render(request, 'Accounts/RestorePassword.html', {'form': form})
    form = RestorePasswordForm()
    return render(request, 'Accounts/RestorePassword.html', {'form': form})


def set_new_password(request, signed_pk):
    try:
        pk = signing.loads(signed_pk, max_age=timedelta(minutes=15))
    except:
        raise Http404

    user = User.objects.get_or_404(pk=pk)

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['spassword'])
            user.save()
            user_auth = authenticate(username=user.email,
                                     password=form.cleaned_data['spassword'])
            auth.login(request, user_auth)
            return redirect('accounts:personal_area')
        return render(request, 'Accounts/SetNewPassword.html', {'form': form})
    form = SetNewPasswordForm()
    return render(request, 'Accounts/SetNewPassword.html', {'form': form})
