from django import views
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response 
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
import jwt
from account.utils import Util
from .serializers import EmailVerificationSerializer, UserSerializer,SignupSerializer,LoginSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from account.helpers import send_otp_to_phone
from account.models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import views,generics
from account.validators import validate_file_extension



# @api_view(['POST'])
# def register(request):
#     data = request.data
#     User = get_user_model()
#     user = SignupSerializer(data=data)
#     if user.is_valid():
#         if not User.objects.filter(username=data['email']).exists():
#             user = User.objects.create(
#                 first_name = data['first_name'],
#                 last_name = data['last_name'],
#                 username = data['email'],
#                 email = data['email'],
#                 phone_number =data['phone_number'],
#                 education = data['education'],
#                 experience = data['experience'],
#                 skill = data['skill'],
#                 role = data['role'],
#                 password = make_password(data['password']),
#                 is_employer=data['is_employer'],
#                 is_employee=data['is_employee'],
#
#             )
#             return Response(
#                 {'message':'User Registered'},
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {'error':'User Already Exists'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#     else:
#         return Response(user.errors)
#         # return HttpResponse('Hii')
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        User = get_user_model()
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)





# @api_view(['POST'])
# def register(request):
#     data = request.data
#     User = get_user_model()
#     user = SignupSerializer(data=data)
#     if user.is_valid():
#         if not User.objects.filter(username=data['email']).exists():
#             user = User.objects.create(
#                 first_name = data['first_name'],
#                 last_name = data['last_name'],
#                 username = data['email'],
#                 email = data['email'],
#                 phone_number =data['phone_number'],
#                 education = data['education'],
#                 experience = data['experience'],
#                 skill = data['skill'],
#                 role = data['role'],
#                 password = make_password(data['password']),
#                 is_employer=data['is_employer'],
#                 is_employee=data['is_employee'],
#                 is_active = False

#             )
#             # User.objects.filter(id=id).update(is_employee=True)

#             print(user.is_active)
#             #Code for Email Auth Starts

#             # serializer = SignupSerializer(data=data)
#             # serializer.is_valid(raise_exception=True)
#             # serializer.save()
#             # print(serializer)
#             #
#             # user_data = serializer.data
#             # print(user_data)
#             user = User.objects.get(email=data['email'])
#             print(user.id)
#             id=user.id
#             # User.objects.filter(id=id).update(is_verified=True)

#             token = RefreshToken.for_user(user).access_token
#             current_site = get_current_site(request).domain
#             relativeLink = reverse('email-verify')
#             absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
#             email_body = 'Hi ' + user.first_name + \
#                          ' Use the link below to verify your email \n' + absurl
#             data = {'email_body': email_body, 'to_email': user.email,
#                     'email_subject': 'Verify your email'}

#             Util.send_email(data)
#             return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(
#                 {'error':'User Already Exists'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#     else:
#         return Response(user.errors)
#         # return HttpResponse('Hii')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user)
    # currentsite = get_current_site(request)
    # print(currentsite)
    return Response(user.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    User = get_user_model()
    user = request.user
    print(user)
    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.username = data['email']
    # User.objects.filter(user=request.user).update(is_admin = True)

    if data['password'] != '':
        user.password = make_password(data['password'])

    if User.objects.filter(username=data['email']).exists():
        return Response(
                {'error':'User Name Already Exists'},
                status=status.HTTP_400_BAD_REQUEST
            )


    user.save()
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAdminUser ])
def authorize_employer(request,id):
    User = get_user_model()
    
    User.objects.filter(id=id).update(is_employer = True)
    User.objects.filter(id=id).update(is_employee = False)

    
  

    try:
        obj = User.objects.get(id=id)
        print(obj)
    except User.DoesNotExist:
        msg = {"msg": "Employer does not exist"}
        return Response(msg,status=status.HTTP_404_NOT_FOUND)

   
    
    serializer = UserSerializer(obj,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



#----------------------OTP CONFIG STARTS------------------------

@api_view(['POST'])
def send_otp(request):
    data = request.data

    if UserProfile.objects.filter(user_id = data['user_id']).exists():
        return Response(
                {'error':'Already Registered'},
                status=status.HTTP_400_BAD_REQUEST
            )



    if data.get('phone_number') is None:
        return Response({
            'status' : 400,
            'message' : 'Phone number is required'
        })


    if data.get('password') is None:
        return Response({
            'status' : 400,
            'message' : 'Password field is required'
        })


    user = UserProfile.objects.create(
        # username = data.get('username'),
        phone_number = data.get('phone_number'),
        resume="",
        user_id=data.get('user_id'),
        is_verified = True,
        # password = data.get('password'),
        otp = send_otp_to_phone(data.get('phone_number'))
        )
    # user.set_password = data.get('set_password')
    user.save()
    return Response({
        'status' : 200,
        'message' : 'OTP has been sent successfully!'
    })


@api_view(['POST'])
def verify_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status' : 400,
            'message' : 'Phone number is required'
        })

    if data.get('otp') is None:
        return Response({
            'status' : 400,
            'message' : 'OTP field is required'
        })

    try:
        user_obj = UserProfile.objects.get(phone_number = data.get('phone_number'))
                
    except Exception as e:
        return Response({
            'status' : 400,
            'message' : 'Invalid number'
        })

    if user_obj.otp == data.get('otp'):
        return Response({
            'status' : 200,
            'message' : 'OTP verified!'
        })

    return Response({
        'status' : 400,
        'message' : 'Invalid OTP'
    })

#----------------------OTP CONFIG ENDS------------------------

#----------------------EMAIL VERIFICATION------------------------
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        User = get_user_model()
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)







class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer


    #  token_param_config = openapi.Parameter(
    #      'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    #
    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        print("Hii")
        data = request.data
        print (data)
        token = request.GET.get('token')
        print(token)
        print("Heyyyy")
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            print(payload)
            User=get_user_model()
            user = User.objects.get(id=payload['user_id'])
            id=user.id
            print(user)
            if not user.is_verified:
                User.objects.filter(id=id).update(is_verified=True)

                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully Registered'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

#________________RESUME UPLOAD_________________

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def uploadResume(request):

    user = request.user
    resume = request.FILES['resume']

    if resume == '':
        return Response({ 'error': 'Please upload your resume.' }, status=status.HTTP_400_BAD_REQUEST)

    isValidFile = validate_file_extension(resume.name)

    if not isValidFile:
        return Response({ 'error': 'Please upload only pdf file.' }, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user, many=False)

    user.userprofile.resume = resume
    user.userprofile.save()

    return Response(serializer.data)


#---------------LOGIN XTRA ----------------------
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

