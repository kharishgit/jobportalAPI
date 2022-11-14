from django.shortcuts import render
from .models import company
from rest_framework.decorators import api_view,permission_classes
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CompanySerializer
from rest_framework import status
from django.shortcuts import get_object_or_404





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_company(request):
    print("jj")

    # request.data['user']= request.user
    print (request.user)
    print("jj")
    if request.user.is_employer != True:
        return Response({'message':'You cannot Add  the job' },status=status.HTTP_403_FORBIDDEN)

    data = request.data
    print (data)
    # cmp = company.objects.create(**data)
    compny = company.objects.create(
                user= request.user,
                company_name =data.get('company_name'),
                website=data.get('website'),
                size = data.get('size'),
                founded = data.get('founded'),
                stage = data.get('stage'),
                about = data.get('about'),
                linked_in = data.get('linked_in'),
            )
    compny.save()
    print(compny)
    serializer = CompanySerializer(compny,many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_details(request):
    queryset = company.objects.all()
    print(queryset)
    serializer = CompanySerializer(queryset,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def company_details_id(request,pk):
    queryset = get_object_or_404(company,id=pk)
    print(queryset)
    serializer = CompanySerializer(queryset,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_company_id(request,pk):
    cmp = get_object_or_404(company,id=pk)
    if cmp.user != request.user:
        return Response({'message':'You cannot Delete the Company Details' },status=status.HTTP_403_FORBIDDEN)
    cmp.delete()
    return Response({'message':'Company is deleted successfully'},
    status=status.HTTP_200_OK)