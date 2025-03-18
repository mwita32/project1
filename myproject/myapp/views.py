from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from .models import CustomUser
from .forms import RegisterForm, LoginForm, PasswordResetForm, SetNewPasswordForm
from .utils import generate_token, encode_uid, decode_uid
import logging

logger = logging.getLogger(__name__)

def homepage(request):
    return render(request, 'homepage.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            user = form.save(commit=False)
            user.is_active = False  # Disable account until email verification
            user.save()

            # Generate verification link
            token = generate_token(user)
            uid = encode_uid(user.pk)
            site = get_current_site(request).domain
            verification_link = f"http://{site}/verify-email/{uid}/{token}/"

            # Debugging log
            logger.info(f"Verification link for {email}: {verification_link}")

            # Send verification email
            subject = "Verify Your Email"
            message = render_to_string("email_verification.html", {"link": verification_link})

            if settings.EMAIL_HOST_USER:
                email_message = EmailMultiAlternatives(subject, "", settings.EMAIL_HOST_USER, [email])
                email_message.attach_alternative(message, "text/html")
                email_message.send()
                messages.success(request, "A verification email has been sent to your email.")
            else:
                messages.error(request, "Email sending failed. Please contact support.")

            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check your details.")
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
            return redirect("login")
        else:
            messages.error(request, "Invalid or expired verification link.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid verification request.")

    return redirect("login")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("homepage")  # Redirect to homepage after login
        else:
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
                login(request, user)
                messages.success(request, "Admin login successful!")
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


def forgot_password_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            try:
                user = CustomUser.objects.get(email=email)

                token = generate_token(user)
                uid = encode_uid(user.pk)
                site = get_current_site(request).domain
                reset_link = f"http://{site}/reset-password/{uid}/{token}/"

                subject = "Password Reset Request"
                message = render_to_string("password_reset.html", {"link": reset_link})

                if settings.EMAIL_HOST_USER:
                    email_message = EmailMultiAlternatives(subject, "", settings.EMAIL_HOST_USER, [email])
                    email_message.attach_alternative(message, "text/html")
                    email_message.send()
                    messages.success(request, "A password reset link has been sent to your email.")
                else:
                    messages.error(request, "Email sending failed. Please contact support.")

                return redirect("login")
            except CustomUser.DoesNotExist:
                messages.error(request, "No account found with that email.")
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
                    return redirect("login")
            else:
                form = SetNewPasswordForm()
            return render(request, "reset_password.html", {"form": form})
        else:
            messages.error(request, "Invalid or expired reset link.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid password reset request.")

    return redirect("forgot_password")


@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")


@login_required
def homepage_view(request):
    return render(request, "homepage.html")
