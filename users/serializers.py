# written by [SENU]:
from rest_framework import serializers
from users.models import User
#[AMS] edited to add token on register and login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from django.conf import settings
import uuid

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'email_verified', 'is_approved']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        
        #[AMS] Generate email verification token
        user.email_verification_token = str(uuid.uuid4())
        user.email_verified = False
        user.is_active = False
        user.save()
        
        #[AMS] Send verification email
        verification_link = f"http://localhost:8000/users/verify-email/{user.email_verification_token}/"
        send_mail(
            'Verify your email',
            f'Click this link to verify your email: {verification_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return user
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Check if email is verified
        if not self.user.email_verified:
            raise serializers.ValidationError("Email not verified. Please check your email for verification link.")
            
        # Add custom claims
        data.update({
            'email': self.user.email,
            'role': self.user.role,
            'name': self.user.name
        })
        return data