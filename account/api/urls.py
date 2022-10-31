from django.urls import path
from account.api import views

from account.api.views import VerifyEmail


urlpatterns =[
    path('register/',views.register,name='register'),
    path('current_user/',views.current_user,name='current_user'),
    path('update_user/',views.update_user,name='update_user'),
    path('send_otp/',views.send_otp,name='send_otp'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('authorize_employer/<str:id>/',views.authorize_employer,name='authorize_employer'),
    # path('emailReg/', RegisterView.as_view(), name="emailReg"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('uploadResume/',views.uploadResume,name='uploadResume'),






]