from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import UsersSerializers


User = get_user_model()

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers