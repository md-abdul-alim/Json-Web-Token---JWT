from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from .serializers import CustomTokenObtainPairSerializer
# Create your views here.


class CustomObtainTokenPairWithPhoneView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CustomTokenObtainPairSerializer

