from django.urls import path, include
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('login/',views.loginView,name='login'),
    path('logout/',views.logoutView,name='logout'),
    path('registration/',views.registrationView,name='registration'),
    path('email_resend/',views.email_resend,name='email_resend'),
    path('conform_email/',views.Conform_Email.as_view(),name='conform_email'),
    path('change_email/',views.Change_Email.as_view(),name='change_email'),
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name="password_reset.html"),name="password_reset"),
    path('password_reset_sent/',auth_view.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),   
    path('block/',views.block,name='block'),
]