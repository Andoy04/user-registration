import jwt
import django_filters
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import User
from .utils import Util
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer

class RegisterView(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['email', 'password', 'first_name', 'last_name', 'is_active']

    def create(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.first_name + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        print(data)
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['email', 'password', 'first_name', 'last_name', 'is_active']

    def list(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            queryset = User.objects.all()
            serializer = RegisterSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response(User.objects.values_list('first_name') , status=status.HTTP_200_OK)
        except jwt.exceptions.DecodeError as identifier:
            return Response(User.objects.values_list('first_name'), status=status.HTTP_200_OK)

class VerifyEmail(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = EmailVerificationSerializer

    def list(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class Modify(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = EmailVerificationSerializer

    def update(self, request):
        request_data = request.data
        token = request_data['token']
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            user.password = request_data['password']
            user.save()
            return Response({'password': 'Successfully changed'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request):
        try:
            request_data = request.data
            user = User.objects.get(email=request_data['email'])
            if not user.is_active:
                token = RefreshToken.for_user(user).access_token
                current_site = get_current_site(request).domain
                relativeLink = reverse('verify')
                absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                email_body = 'Hi '+user.first_name + \
                    ' Use the link below to verify your email \n' + absurl
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Verify your email'}

                print(data)
                Util.send_email(data)
                return Response('Inactive user', status=status.HTTP_400_BAD_REQUEST)

            if(user.check_password(request_data['password'])):
                return Response(user.tokens(), status=status.HTTP_200_OK)
            else:
                return Response('Invalid password', status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response('Invalid user', status=status.HTTP_400_BAD_REQUEST)