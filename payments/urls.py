from django.urls import path
from .import views

urlpatterns = [
    path('<int:pk>/',views.payment, name='payment'),
    path('status/', views.payment_status,name='payment-status'),
    path('success_payments/', views.success_payments,name='success_payments'),
    path('feedback/<int:pk>/', views.feedback),
    path('display_feedback/', views.display_feedback)
]