from django.contrib.auth import (login as django_login,
                                 logout as django_logout)
from django.contrib.auth.models import User
from .permissions import IsCurrentUserOrReadOnly
from .serializers import LoginSerializer, UserSerializer, ProfileUserSerializer
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView, RetrieveAPIView


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        django_login(request, user=user)

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)

        return Response(status=204)


class ProfileUpdateView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCurrentUserOrReadOnly, permissions.IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = ProfileUserSerializer

    def get_object(self):
        return self.request.user.profile

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class GetProfileByIdView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileUserSerializer
    lookup_field = 'pk'
    queryset = User.objects.filter(is_active=True)


class GetProfileByUsernameView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileUserSerializer
    lookup_field = 'username'

    queryset = User.objects.filter(is_active=True)


class UserDeleteView(APIView):
    permission_classes = (IsCurrentUserOrReadOnly,
                          permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None, *args, **kwargs):
        try:
            User.objects.get(pk=request.user.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_409_CONFLICT)
