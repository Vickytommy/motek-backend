from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

def index(request):
    return render(request, "motek/index.html")

def users(request):
    users = User.objects.all()
    return render(request, "motek/register.html", {"users": users})

