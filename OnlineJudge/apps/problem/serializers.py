from rest_framework import serializers
from .models import Problem

class ProblemSerialer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"