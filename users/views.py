from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# CRUD user: create, read ,update ,delete
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        user.email_verified = True
        user.email_verification_token = None
        user.is_active = True
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
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