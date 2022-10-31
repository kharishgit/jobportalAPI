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