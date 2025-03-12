from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]