from account.models import UserProfile
from dataclasses import fields
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('first_name', 'last_name', 'email', 'password','role')
        extra_kwrgs = {
            'first_name':{'required': True,'allow_blank':False},
            'last_name':{'required': True,'allow_blank':False},
            'email':{'required': True,'allow_blank':False},
            'role': {'required': True, 'allow_blank': False},

            'password':{'required': True,'allow_blank':False,'min_length': 6,'write_only':True },
        }
        def validate_password(self,value):
                if len(value)<4:
                    raise serializers.ValidationError("Password must be minimum 4 characters")
                else:
                    return value
        def save(self):
            reg = User(
                username=self.validated_data['username'],
                role=self.validated_data['role'],

            )
            password=self.validated_data['password'],

            reg.set_password(password)
            reg.save()
            return 

class UserSerializer(serializers.ModelSerializer):
    resume = serializers.CharField(source='userprofile.resume')
    otp = serializers.CharField(source='userprofile.otp')
    is_verified = serializers.BooleanField(source='userprofile.is_verified')
    phone_number = serializers.CharField(source='userprofile.phone_number')

    class Meta:
        User = get_user_model()
        model = User
        #Have to add user profile 
        fields = ('first_name', 'last_name', 'email', 'username','resume','phone_number','is_verified','otp','is_employer')
        
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        User = get_user_model()
        model = User
        fields = ['token']

#-------------Login Xtra ----------------
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        User = get_user_model()
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        User = get_user_model()
        model = User
        fields = ['email', 'username', 'password','phone_number','skill','is_employee','is_employer','first_name','last_name','education','experience','time_period']
        # fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        User = get_user_model()
        return User.objects.create_user(**validated_data)

