# written by [SENU]:
from rest_framework import serializers
from users.models import User
#[AMS] edited to add token on register and login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class UserSerializer(serializers.ModelSerializer):
    # [AMS] accept national_id_image_path in input when role is doctor
    national_id_image_path = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'email_verified', 'is_approved', 'national_id_image_path']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # [AMS] ensure national_id_image_path is provided when role is doctor
        if data.get('role') == 'doctor' and not data.get('national_id_image_path'):
            raise serializers.ValidationError({'national_id_image_path': 'This field is required for doctors.'})
        return data

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        validated_data.pop('national_id_image_path', None)  # Remove image field, handled by view
        user = User(**validated_data)
        user.set_password(password)
        
        #[AMS] Generate email verification token
        user.email_verification_token = str(uuid.uuid4())
        user.email_verified = False
        user.is_active = False
        user.save()
        
        #[AMS] Send verification email
        verification_link = f"http://localhost:8000/users/verify-email/{user.email_verification_token}/"
        html_content = render_to_string('emails/email_verification.html', {
            'user': user,
            'verification_link': verification_link,
        })
        
        # Render plain text content
        text_content = strip_tags(render_to_string('emails/email_verification.txt', {
            'user': user,
            'verification_link': verification_link,
        }))
        
        # Create and send email
        email = EmailMultiAlternatives(
            'Verify your email',
            text_content,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
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