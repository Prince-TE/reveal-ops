from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from reveal_app.models import CustomUser
from reveal_app.serializers import CustomUserSerializer,LoginSerializer,SetPasswordSerializer

# Create your views here.

@swagger_auto_schema(
    method='get',
    operation_description="A simple ping endpoint to check if the server is running.",
    responses={200: 'Ping successful response with a message'}
)
@api_view(['GET'])
def ping_view(request):
    return Response({'message':'ping successful'},status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: 'Login Successful', 400: 'Invalid Credentials'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
        
        if user.first_login:
            return Response({'message':'Please set your password first'}, status=status.HTTP_200_OK)
        
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'message':'Login Successful. Redirecting to dashboard',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=SetPasswordSerializer,
    responses={200: 'Password set successfully', 400: 'User does not exist'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def set_password_view(request):
    serializer = SetPasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error':'User does not exist'},status=status.HTTP_400_BAD_REQUEST)
        
        if user.first_login:
            user.set_password(password)
            user.first_login = False
            user.save()
            return Response({'message':'Password set successfully. You can now log in'},status=status.HTTP_200_OK)
        
        return Response({'message':'Password already set. Please log in'},status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
