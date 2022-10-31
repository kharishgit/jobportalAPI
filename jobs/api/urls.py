from django.urls import path
from jobs.api import views


urlpatterns = [
    path('jobview/',views.getjobs,name='jobview'),
    path('add_job/',views.add_job,name='add_job'),
    path('get_jobs_id/<str:pk>/',views.get_jobs_id,name='get_jobs_id'),
    path('update_job/<str:pk>/',views.update_job,name='update_job'),
    path('delete_jobs_id/<str:pk>/',views.delete_jobs_id,name='delete_jobs_id'),
    path('apply_job/<str:pk>/',views.apply_job,name='apply_job'),
    path('get_jobs_applied/',views.get_jobs_applied,name='get_jobs_applied'),
    path('isApplied/<str:pk>/',views.isApplied,name='isApplied'),
    path('job_stat/<str:topic>/',views.job_stat,name='job_stat'),
    path('posted_jobs/',views.posted_jobs,name='posted_jobs'),
    path('candidatesApplied/<str:pk>/',views.candidatesApplied,name='candidatesApplied'),
    path('filter_jobs/',views.filter_jobs,name='filter_jobs'),
    path('job_suggestion/',views.job_suggestion,name='job_suggestion'),








]
