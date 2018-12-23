# from django.shortcuts import render
from app import models
from app import serializer
# from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator

# Create your views here.

class UserViews(APIView):
    def get(self, request, format=None):
        users = models.User.objects.all()
        userSerializer = serializer.UserSerializer(users, many=True)
        return Response(userSerializer.data)

class login(APIView):
    def get(self, request, format=None):
        
