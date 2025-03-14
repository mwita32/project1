from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RegisterForm(UserCreationForm):
    reg_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["reg_number", "email", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        """Override save() to set username as reg_number"""
        user = super().save(commit=False)
        user.username = user.reg_number  # Automatically set username to reg_number
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Registration Number")

    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()
        if user and not user.is_verified:
            raise forms.ValidationError("Please verify your email before logging in.")
        return cleaned_data

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Enter your email", required=True)

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
