from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        reg_number = request.POST['reg_number']
        password = request.POST['password']
        user = authenticate(request, username=reg_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid registration number or password')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render(request, 'register.html')

def admin_login_view(request):
    return render(request, 'admin_login.html')

def forgot_password_view(request):
    return render(request, 'forgot_password.html')

def password_reset_view(request):
    return render(request, 'password_reset.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')
