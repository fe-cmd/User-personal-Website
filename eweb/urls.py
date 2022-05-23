from django.urls import path
from .import views
from .views import RequestPasswordResetEmail, VerificationView, LoginView, EmailValidationView, UsernameValidationView, CompletePasswordReset
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('home', views.home, name='home'),
    path('index', views.index, name='index'),
    path('tech', views.tech, name='tech'),
    path('about', views.about, name='about'),
    path('product', views.product, name='product'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('password_reset_form', RequestPasswordResetEmail.as_view(), name='password_reset_form'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('set-new-password/<uidb64>/<token>',csrf_exempt(CompletePasswordReset.as_view()), name='reset_user_password')
    #path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('sent_email', views.sent_email, name='sent_email')
]
