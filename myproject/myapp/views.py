from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from .models import CustomUser
from .forms import RegisterForm, LoginForm, PasswordResetForm, SetNewPasswordForm
from .utils import generate_token, encode_uid, decode_uid



def home_view(request):
    return redirect('login')  # Redirect to the login page

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")  # Ensure email is retrieved safely
            print(f"Debug: Retrieved email -> {email}")  # Debug print
            user = form.save(commit=False)
            user.is_active = False  # Disable account until email verification
            user.save()
            token = generate_token(user)
            uid = encode_uid(user.pk)
            site = get_current_site(request).domain
            link = f"http://{site}/verify-email/{uid}/{token}/"
            subject = "Verify Your Email"
            message = render_to_string("email_verification.html", {"link": link})



            email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [email])

            email.attach_alternative(message, "text/html")
            email.send()
            messages.success(request, "A verification email has been sent to your email.")
            print(f"Registration successful for user: {user.username}")  # Debug print
            return redirect("login")
        else:
            print("Registration form is not valid")  # Debug print
            print(form.errors)  # Print form errors
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def verify_email(request, uid, token):
    try:
        uid = decode_uid(uid)
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.is_active = True
            user.save()
            messages.success(request, "Your email has been verified! You can now log in.")
            print(f"Email verified for user: {user.username}")  # Debug print
            return redirect("login")
        else:
            messages.error(request, "Invalid or expired verification link.")
            print("Invalid or expired verification link")  # Debug print
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid verification request.")
        print("Invalid verification request")  # Debug print
    return redirect("login")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(f"User authenticated: {user.username}")  # Debug print
            login(request, user)
            return redirect("dashboard")
        else:
            print("Login form is not valid")  # Debug print
            print(form.errors)  # Print form errors
            messages.error(request, "Invalid credentials. Try again.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def admin_login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_admin:
                print(f"Admin login successful for user: {user.username}")  # Debug print
                login(request, user)
                return redirect("admin_dashboard")
            else:
                messages.error(request, "You are not an admin.")

    else:
        form = LoginForm()
    return render(request, "admin_login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")


import logging

logger = logging.getLogger(__name__)


def forgot_password_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            print(f"DEBUG: Retrieved email -> {email}")  # Debugging Print

            if not email:
                messages.error(request, "Invalid email.")
                return redirect("forgot_password")

            try:
                user = CustomUser.objects.get(email=email)
                print(f"DEBUG: Found user -> {user.username}")  # Debugging Print

                token = generate_token(user)
                uid = encode_uid(user.pk)
                site = get_current_site(request).domain
                reset_link = f"http://{site}/reset-password/{uid}/{token}/"

                subject = "Password Reset Request"
                message = render_to_string("password_reset.html", {"link": reset_link})

                recipient_email = [email]
                print(f"DEBUG: Sending email to {recipient_email}")  # Debugging Print

                email_message = EmailMultiAlternatives(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # Email sender
                    recipient_email  # Email recipient
                )
                email_message.attach_alternative(message, "text/html")
                email_message.send()

                print("DEBUG: Email sent successfully!")  # Debugging Print
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect("login")

            except CustomUser.DoesNotExist:
                messages.error(request, "No account found with that email.")
                print("DEBUG: No account found with that email")  # Debugging Print

    else:
        form = PasswordResetForm()

    return render(request, "forgot_password.html", {"form": form})

def reset_password_view(request, uid, token):
    try:
        uid = decode_uid(uid)
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = SetNewPasswordForm(request.POST)
                if form.is_valid():
                    user.set_password(form.cleaned_data["new_password"])
                    user.save()
                    messages.success(request, "Your password has been reset. You can now log in.")
                    print(f"Password reset for user: {user.username}")  # Debug print
                    return redirect("login")
            else:
                form = SetNewPasswordForm()
            return render(request, "reset_password.html", {"form": form})
        else:
            messages.error(request, "Invalid or expired reset link.")
            print("Invalid or expired reset link")  # Debug print
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid password reset request.")
        print("Invalid password reset request")  # Debug print
    return redirect("forgot_password")

@login_required
def dashboard_view(request):
    print(f"Dashboard accessed by user: {request.user.username}")  # Debug print
    return render(request, "dashboard.html")
