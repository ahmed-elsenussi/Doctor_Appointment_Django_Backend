from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import AccessToken
from doctors.models import Doctor
from patients.models import Patient
from django.contrib.auth import get_user_model
from django.db import transaction  # [SENU] Added for atomicity
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import render
# CRUD user: create, read ,update ,delete
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    #[AMS] we need to override the create method to handle create doctor or patient profile 
    def create(self, request, *args, **kwargs):
        with transaction.atomic():  # [SENU] Ensure atomicity
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            role = request.data.get('role', 'patient')
            
            if role == 'doctor':
                # first recieve national_id_image_path and doctor_image_path (optional)
                national_id_image_path = request.FILES.get('national_id_image_path')
                doctor_image_path = request.FILES.get('doctor_image_path')  # Optional
                if not national_id_image_path:
                    user.delete()  # Rollback user creation
                    return Response(
                        {'error': 'National ID image is required for doctor registration'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # [SENU] Use get_or_create to prevent duplicate Doctor records
                doctor, created = Doctor.objects.get_or_create(
                    doctor_id=user,
                    defaults={
                        'national_id_image_path': national_id_image_path,
                        'doctor_image_path': doctor_image_path
                    }
                )
                if not created and (national_id_image_path or doctor_image_path):
                    # Update images if provided
                    if national_id_image_path:
                        doctor.national_id_image_path = national_id_image_path
                    if doctor_image_path:
                        doctor.doctor_image_path = doctor_image_path
                    doctor.save()
            
            elif role == 'patient':
                date_of_birth = request.data.get('date_of_birth')
                patient_image_path = request.FILES.get('patient_image_path')
                if not date_of_birth or not patient_image_path:
                    user.delete()  # Rollback user creation
                    return Response(
                        {'error': 'Both date of birth and patient image are required for patient registration'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                Patient.objects.create(
                    patient_id=user,
                    date_of_birth=date_of_birth,
                    patient_image_path=patient_image_path
                )
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

@api_view(['GET'])
def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        user.email_verified = True
        user.email_verification_token = None
        user.is_active = True
        user.save()
        return render(request, 'accounts/email_confirmed.html')
    except User.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/auth/google/callback"
    client_class = OAuth2Client

@api_view(['POST'])
def google_authenticate(request):
    try:
        email = request.data.get('email')
        name = request.data.get('name')
        role = request.data.get('role', 'patient')  # Default to 'patient' if not provided
        
        # Check if user exists
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'email_verified': True,  # Trust Google's verification
                'is_active': True,
                'role': role,  
            }
        )
        
        if created:
            # New user - set a random password (user won't need it)
            user.set_password(str(uuid.uuid4()))
            user.save()
        
        # Generate token for the user
        refresh = MyTokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework_simplejwt.views import TokenObtainPairView
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        
           # First check if user exists and is_active status
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Check if email is verified (which would make is_active=True)
            if not user.email_verified:
                return Response({
                    'error': 'email_not_verified',
                    'detail': 'Please verify your email before logging in',
                    'email': user.email
                }, status=status.HTTP_403_FORBIDDEN)
                
            # Check if account is active (should be true if email verified)
            if not user.is_active:
                return Response({
                    'error': 'account_inactive',
                    'message': 'Account is not active'
                }, status=status.HTTP_403_FORBIDDEN)
                
        except User.DoesNotExist:
            # Don't reveal whether user exists for security
            pass
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            try:
                # Decode the access token to get user ID
                access_token = AccessToken(response.data['access'])
                user_id = access_token['user_id']
                
                # Get the user object
                user = User.objects.get(id=user_id)
                
                # Add user data to the response
                response.data['user'] = {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,  
                    'role': user.role,  # make sure your User model has this field
                }
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

        return response

#[OKS] this view is used to get the current user details
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


    