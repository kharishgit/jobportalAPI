from django.urls import path
from . import views
urlpatterns =[
    path('add_company/', views.add_company, name='add_company'),
    path('company_details/', views.company_details, name='company_details'),
    path('company_details_id/<str:pk>/', views.company_details_id, name='company_details_id'),
    path('delete_company_id/<str:pk>/', views.delete_company_id, name='delete_company_id'),

]