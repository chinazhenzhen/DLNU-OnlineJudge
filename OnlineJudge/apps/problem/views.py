from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ProblemSerialer
from .models import Problem

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerialer

