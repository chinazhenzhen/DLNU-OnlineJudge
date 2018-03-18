from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import UsersSerializer,UserChangePasswordSerializer


User = get_user_model()

class UsersViewSet(viewsets.ModelViewSet): #默认开启get post 等操作
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class UserChangePasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer