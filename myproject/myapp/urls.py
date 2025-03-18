from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("homepage/", views.homepage_view, name="homepage"),  # Updated to use homepage_view
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('verify-email/<str:uid>/<str:token>/',views.verify_email, name='verify_email'),
]
