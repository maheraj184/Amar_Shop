from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, login_view, logout_view, profile_view

urlpatterns = [
    # User account
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

path(
    'forgot-password/',
    auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ),
    name='password_reset'
),

path(
    'password_reset_sent/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ),
    name='password_reset_complete'
),

]
