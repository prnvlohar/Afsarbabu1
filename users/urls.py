from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from users.views import (ActivateView, LoginView, RegisterView,
                         create_users, index_view, LinkView, InstituteRegisterView,
                         logout_view, UsersView, payment_success_view, payment_view)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('link/', LinkView.as_view(), name='link'),
    path('institute-reg/', InstituteRegisterView.as_view(), name='institute_reg'),
    path('activate/<uidb64>/<token>',
         ActivateView.as_view(), name='activate'),
    path('home/', index_view, name='index'),
    path('logout/', logout_view, name='logout'),
    path('create_users/<int:num_users>/', 
         create_users, name='create_users'),
    path('users/', UsersView.as_view(), name='users'),
    # path('ref_code/', ReferralCodeView.as_view(), name='ref_code'),

    # forgot password urls

    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset.html'),
        name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    path('payment/', payment_view, name='payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
]
