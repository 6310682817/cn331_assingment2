from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .page import AdminPage, StudentPage

# login page
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'reg/login.html', {
                'message': 'Invalid credentials.'
            })
    return render(request, 'reg/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# index page
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        if str(request.user) == "admin":
            return AdminPage(request).index()
        else:
            return StudentPage(request).index()

# admin page
def admin_search(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return AdminPage(request).search()

def student(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return AdminPage(request).student()

def checkStu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return AdminPage(request).checkStu()

def checkSub(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return AdminPage(request).checkSub()

# student page
def search(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return StudentPage(request).search()

def status(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return StudentPage(request).status()

def quota(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return StudentPage(request).quota()
