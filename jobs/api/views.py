from re import T
import re
from turtle import title

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from jobs.models import Experience, jobType
from jobs.models import CandidatesApplied
from django.db.models import Avg, Min, Max, Count
from django.db.models import Q
from .filters import jobFilter
from jobs.models import jobs

from .serializers import CandidatesAppliedSerializer, jobSerializer



@api_view(['GET'])
def getjobs(request):
    job = jobs.objects.all()
    serializer = jobSerializer(job,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_jobs_id(request,pk):
    job = get_object_or_404(jobs,id=pk)
    serializer = jobSerializer(job,many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_job(request):
    request.data['user']= request.user
    if request.user.is_employer != True:
        return Response({'message':'You cannot Add  the job' },status=status.HTTP_403_FORBIDDEN)

    data = request.data
    job = jobs.objects.create(**data)
    serializer = jobSerializer(job,many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request,pk):
    job = get_object_or_404(jobs,id=pk)

    if job.user != request.user:
        return Response({'message':'You cannot update the job' },status=status.HTTP_403_FORBIDDEN)
    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.jobType = request.data['jobType']
    job.education = request.data['education']
    job.Industry = request.data['Industry']
    job.Experience = request.data['Experience']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']
    job.save()
    serializer = jobSerializer(job,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_jobs_id(request,pk):
    job = get_object_or_404(jobs,id=pk)
    if job.user != request.user:
        return Response({'message':'You cannot Delete the job' },status=status.HTTP_403_FORBIDDEN)
    job.delete()
    return Response({'message':'Job is deleted successfully'},
    status=status.HTTP_200_OK)


@api_view(['GET'])
def job_stat(request,topic):
    args = { 'title__icontains': topic }
    job =jobs.objects.filter(**args)
    if len(job)==0:
        return Response({'message' :'No stats Found for {topic}'.format(topic=topic)})

    stat = job.aggregate(
        total_jobs=Count('title'),
        avg_positions =Avg('positions'),
        avg_salary =Avg('salary'),
        min_salary =Min('salary'),
        max_salary =Max('salary')

    )
    return Response(stat)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job(request,pk):
    user = request.user
    print(user)
    print(user.is_employee)
    chk = CandidatesApplied.objects.all().values()
    print(chk)

    # userprofile= CandidatesApplied.objects.filter(user__username=user).exists()
    # print(userprofile)
    # if not userprofile:
    #     return Response({ 'error': 'Upload Your resume First' }, status=status.HTTP_400_BAD_REQUEST)
    #


    dat=jobs.objects.filter(pk=pk).values()
    # print(dat)
    for i in dat:
        employer_id = i['user_id']
    print(employer_id,"Employer Id")
    cnt=CandidatesApplied.objects.filter(jobs__user=employer_id).count()
    print(cnt,"Jobs")

    User=get_user_model()
    data = User.objects.filter(pk=employer_id).values()
    for time_period in data:
        tim = time_period['time_period']
    print(tim,"Time period for the employer")
    if (tim==3 and cnt == 1 or tim == 6 and cnt == 2):
        return Response({ 'error': 'This Employer cannot receive any more Applicants' }, status=status.HTTP_400_BAD_REQUEST)


   
    if request.user.is_employee !=True:
        return Response({ 'error': 'You are not allowed to apply for Jobs' }, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.is_active != True:
        return Response({ 'error': 'Add Your Resume and verify your Mobile Number' }, status=status.HTTP_400_BAD_REQUEST)

    job = get_object_or_404(jobs,id=pk)
    if user.userprofile.resume == '':
        return Response({ 'error': 'Please upload your resume first' }, status=status.HTTP_400_BAD_REQUEST)



    if job.last_date < timezone.now():
        return Response({'error':'Date for application is passed'},status=status.HTTP_400_BAD_REQUEST)
    alreadyapplied = job.candidatesapplied_set.filter(user=user).exists()
    if alreadyapplied:
        return Response({'error':'You Have Already applied'},status=status.HTTP_400_BAD_REQUEST)

    jobApplied = CandidatesApplied.objects.create(
        jobs=job,
        user=user,
        resume =user.userprofile.resume

    )
    return Response({
        'Applied':True,
        'job_id':jobApplied.jobs_id,
        },status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_jobs_applied(request):
#     args ={'user_id':request.user.id}
#     jobs = CandidatesApplied.objects.filter(**args)
#     serializer =CandidatesAppliedSerializer(jobs,many=True)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_jobs_applied(request):
    args = { 'user_id': request.user.id }
    job = CandidatesApplied.objects.filter(**args)
    serializer = CandidatesAppliedSerializer(job, many=True)
    print(serializer.data)
    return Response(serializer.data)
    






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def isApplied(request, pk):

    user = request.user
    
    job = get_object_or_404(jobs, id=pk)

    applied = job.candidatesapplied_set.filter(user=user).exists()

    return Response(applied)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posted_jobs(request):
    args = {'user': request.user.id}
    job = jobs.objects.filter(**args)
    serializer = jobSerializer(job, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def candidatesApplied(request, pk):

    user = request.user
    if request.user.is_employer !=True:
        return Response({ 'error': 'You cant View the  Candidates Applied' }, status=status.HTTP_400_BAD_REQUEST)
    print(user)
    job = get_object_or_404(jobs, id=pk)
    print(job.user)
    if job.user != user:
        return Response({'error':'You are not authorized to perform this action'},status=status.HTTP_403_FORBIDDEN)
    candidates = job.candidatesapplied_set.all()
    serializer = CandidatesAppliedSerializer(candidates,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def filter_jobs(request):
    filterset = jobFilter(request.GET,queryset=jobs.objects.all().order_by('id'))
    count = filterset.qs.count()
    serializer = jobSerializer(filterset.qs,many=True)
    return Response({
        'Count':count,
        'Jobs':serializer.data})



    


#Filter Jobs on Users Details

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def job_filter_on_userdetail(request):
#     args = { 'user_id': request.user.id }

#     job =jobs.objects.filter(Q(education='') | Q(Experience='') | Q(title='') | Q(jobType='')  ).values()
   

    

    
#     return Response(stat)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_suggestion(request):
    print(request.user.id)
    skill=request.user.skill
    var =skill.split()
    # skill='Flutter'
    print(skill)
    edu = request.user.education

    # args = jobs.objects.filter(title__icontains=var[0])
    args = jobs.objects.filter(title__icontains=var[0]).filter(education=edu)

    print({
        'user':request.user.skill,
    })
    skill=request.user.skill


    # job = jobs.objects.filter(**args)
    serializer = jobSerializer(args, many=True)
    print(serializer.data)
    return Response(serializer.data)