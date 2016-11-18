from django.shortcuts import render, redirect, HttpResponse
from . import models
from .models import Logins
import bcrypt
from django.contrib import messages
import re
from django.contrib.messages import get_messages
NAME_REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'login/index.html')

def add_user(request):
    post = request.POST
    validation = True

    if len(post['first_name']) < 2:
        messages.add_message(request, messages.ERROR, 'First Name Field Must Be At Least 2 Characters Long!')
        validation = False
    elif not NAME_REGEX.match(post['first_name']):
        messages.add_message(request, messages.ERROR, 'First Name Must Contain Only Letters!')
        validation = False

    if len(post['last_name']) < 2:
        messages.add_message(request, messages.ERROR, 'Last Name Field Must Be At Least 2 Characters Long!')
        validation = False
    elif not NAME_REGEX.match(post['last_name']):
        messages.add_message(request, messages.ERROR, 'Last Name Must Contain Only Letters!')
        validation = False

    if len(post['password']) < 8:
        messages.add_message(request, messages.ERROR, 'Password Must Be At Least 8 Characters!')
        validation = False

    if post['password'] != post['pass_confirm']:
        messages.add_message(request, messages.ERROR, 'Your Passwords Did Not Match!')
        validation = False

    if not EMAIL_REGEX.match(post['email']):
        messages.add_message(request, messages.ERROR, 'Your Email Must Be In Proper Format!')
        validation = False

    if models.Logins.objects.all() and validation:
        check = models.Logins.objects.filter(email=post['email'])
        if check:
            if post['email'] == check[0].email:
                messages.add_message(request, messages.ERROR, 'Email is Invalid!')
                validation = False

    if validation:
        password = post['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        Logins.objects.create(first_name=post['first_name'], last_name=post['last_name'], email=post['email'], password=hashed)
    return redirect('/')

def verify_user(request):
    validation = True
    passcheck = request.POST['logcheckpass']

    if models.Logins.objects.all():
        check = models.Logins.objects.filter(email=request.POST['email'])
    else:
        messages.add_message(request, messages.ERROR, 'There Are No Users in the Database!')
        validation = False
    if check:
        if check[0].password == bcrypt.hashpw(passcheck.encode('utf-8'), check[0].password.encode('utf-8')):
            context = {
                        'user': check[0]
            }
        else:
            messages.add_message(request, messages.ERROR, 'Your Password is Incorrect!')
            validation = False
    else:
        messages.add_message(request, messages.ERROR, 'This Email Does Not Exist In the Database!')
        validation = False
    if validation:
        return render(request, 'login/success.html', context)
    else:
        return redirect('/')
